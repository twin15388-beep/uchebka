using CoffeeShop.Models;
using Microsoft.Data.Sqlite;

namespace CoffeeShop.Data;

public static class UserRepository
{
    public static User? FindByLogin(string login)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT id, login, password_hash, salt, full_name, role
            FROM users WHERE login = $login;
            ";
        command.Parameters.AddWithValue("$login", login);

        using var reader = command.ExecuteReader();
        return reader.Read() ? ReadUser(reader) : null;
    }

    public static List<User> GetAll()
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT id, login, password_hash, salt, full_name, role
            FROM users ORDER BY full_name;
            ";
        var users = new List<User>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            users.Add(ReadUser(reader));
        }
        return users;
    }

    private static User ReadUser(SqliteDataReader reader) => new()
    {
        Id = reader.GetInt32(0),
        Login = reader.GetString(1),
        PasswordHash = reader.GetString(2),
        Salt = reader.GetString(3),
        FullName = reader.GetString(4),
        Role = reader.GetString(5)
    };
}

public static class MenuRepository
{
    public static List<MenuItem> GetAll()
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT id, name, category, price, is_available
            FROM menu_items ORDER BY category, name;
            ";
        var items = new List<MenuItem>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            items.Add(new MenuItem
            {
                Id = reader.GetInt32(0),
                Name = reader.GetString(1),
                Category = reader.GetString(2),
                Price = reader.GetDecimal(3),
                IsAvailable = reader.GetInt32(4) == 1
            });
        }
        return items;
    }

    public static void Save(MenuItem item)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = item.Id == 0
            ? @"
              INSERT INTO menu_items (name, category, price, is_available)
              VALUES ($name, $category, $price, $available);
              "
            : @"
              UPDATE menu_items
              SET name = $name, category = $category,
                  price = $price, is_available = $available
              WHERE id = $id;
              ";
        command.Parameters.AddWithValue("$name", item.Name);
        command.Parameters.AddWithValue("$category", item.Category);
        command.Parameters.AddWithValue("$price", item.Price);
        command.Parameters.AddWithValue("$available", item.IsAvailable ? 1 : 0);
        if (item.Id != 0)
        {
            command.Parameters.AddWithValue("$id", item.Id);
        }
        command.ExecuteNonQuery();
    }

    public static void Delete(int id)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = "DELETE FROM menu_items WHERE id = $id;";
        command.Parameters.AddWithValue("$id", id);
        command.ExecuteNonQuery();
    }
}

public static class TableRepository
{
    public static List<CafeTable> GetAll()
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT id, number, seats FROM tables ORDER BY number;
            ";
        var tables = new List<CafeTable>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            tables.Add(new CafeTable
            {
                Id = reader.GetInt32(0),
                Number = reader.GetInt32(1),
                Seats = reader.GetInt32(2)
            });
        }
        return tables;
    }
}

public static class ShiftRepository
{
    public static Shift? GetCurrent()
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT s.id, s.opened_at, s.closed_at, s.user_id, u.full_name
            FROM shifts s JOIN users u ON u.id = s.user_id
            WHERE s.closed_at IS NULL
            ORDER BY s.opened_at DESC LIMIT 1;
            ";
        using var reader = command.ExecuteReader();
        return reader.Read() ? ReadShift(reader) : null;
    }

    public static int Open(int userId)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            INSERT INTO shifts (opened_at, closed_at, user_id)
            VALUES ($opened, NULL, $user);
            ";
        command.Parameters.AddWithValue("$opened",
            DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
        command.Parameters.AddWithValue("$user", userId);
        command.ExecuteNonQuery();
        return (int)connection.LastInsertRowId();
    }

    public static void Close(int shiftId)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            UPDATE shifts SET closed_at = $closed WHERE id = $id;
            ";
        command.Parameters.AddWithValue("$closed",
            DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
        command.Parameters.AddWithValue("$id", shiftId);
        command.ExecuteNonQuery();
    }

    public static List<Shift> GetClosed()
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT s.id, s.opened_at, s.closed_at, s.user_id, u.full_name
            FROM shifts s JOIN users u ON u.id = s.user_id
            WHERE s.closed_at IS NOT NULL
            ORDER BY s.opened_at DESC;
            ";
        var shifts = new List<Shift>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            shifts.Add(ReadShift(reader));
        }
        return shifts;
    }

    public static decimal GetRevenue(int shiftId)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT COALESCE(SUM(total), 0) FROM orders
            WHERE shift_id = $id AND status = 'paid';
            ";
        command.Parameters.AddWithValue("$id", shiftId);
        return Convert.ToDecimal(command.ExecuteScalar());
    }

    private static Shift ReadShift(SqliteDataReader reader) => new()
    {
        Id = reader.GetInt32(0),
        OpenedAt = DateTime.Parse(reader.GetString(1)),
        ClosedAt = reader.IsDBNull(2)
            ? null
            : DateTime.Parse(reader.GetString(2)),
        UserId = reader.GetInt32(3),
        UserName = reader.GetString(4)
    };
}

public static class OrderRepository
{
    public static int Save(Order order, string status = "paid")
    {
        using var connection = Database.Open();
        using var transaction = connection.BeginTransaction();

        var command = connection.CreateCommand();
        command.Transaction = transaction;
        command.CommandText = @"
            INSERT INTO orders
                (shift_id, table_id, order_type, created_at, total, status)
            VALUES ($shift, $table, $type, $created, $total, $status);
            ";
        command.Parameters.AddWithValue("$shift", order.ShiftId);
        command.Parameters.AddWithValue("$table",
            (object?)order.TableId ?? DBNull.Value);
        command.Parameters.AddWithValue("$type", order.OrderType);
        command.Parameters.AddWithValue("$created",
            order.CreatedAt.ToString("yyyy-MM-dd HH:mm:ss"));
        command.Parameters.AddWithValue("$total", order.Total);
        command.Parameters.AddWithValue("$status", status);
        command.ExecuteNonQuery();
        var orderId = (int)connection.LastInsertRowId();

        foreach (var item in order.Items)
        {
            var itemCommand = connection.CreateCommand();
            itemCommand.Transaction = transaction;
            itemCommand.CommandText = @"
                INSERT INTO order_items
                    (order_id, menu_item_id, name, modifiers,
                     quantity, price)
                VALUES ($order, $menu, $name, $mods, $qty, $price);
                ";
            itemCommand.Parameters.AddWithValue("$order", orderId);
            itemCommand.Parameters.AddWithValue("$menu", item.MenuItemId);
            itemCommand.Parameters.AddWithValue("$name", item.Name);
            itemCommand.Parameters.AddWithValue("$mods", item.Modifiers);
            itemCommand.Parameters.AddWithValue("$qty", item.Quantity);
            itemCommand.Parameters.AddWithValue("$price", item.Price);
            itemCommand.ExecuteNonQuery();
        }

        transaction.Commit();
        return orderId;
    }

    public static List<Order> GetByShift(int shiftId)
    {
        using var connection = Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT id, table_id, order_type, created_at, total, status
            FROM orders WHERE shift_id = $shift ORDER BY created_at;
            ";
        command.Parameters.AddWithValue("$shift", shiftId);
        var orders = new List<Order>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            orders.Add(new Order
            {
                Id = reader.GetInt32(0),
                ShiftId = shiftId,
                TableId = reader.IsDBNull(1)
                    ? null
                    : reader.GetInt32(1),
                OrderType = reader.GetString(2),
                CreatedAt = DateTime.Parse(reader.GetString(3)),
                Total = reader.GetDecimal(4),
                Status = reader.GetString(5)
            });
        }
        return orders;
    }
}
