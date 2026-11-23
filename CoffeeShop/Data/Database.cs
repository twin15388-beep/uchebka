using CoffeeShop.Services;
using Microsoft.Data.Sqlite;

namespace CoffeeShop.Data;

/// <summary>
/// Отвечает за подключение к базе данных и её первоначальную инициализацию.
/// </summary>
public static class Database
{
    public const string FileName = "coffeeshop.db";

    public static string ConnectionString => $"Data Source={FileName}";

    public static SqliteConnection Open()
    {
        var connection = new SqliteConnection(ConnectionString);
        connection.Open();
        return connection;
    }

    public static void Initialize()
    {
        using var connection = Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'barista'))
            );

            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                is_available INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL UNIQUE,
                seats INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opened_at TEXT NOT NULL,
                closed_at TEXT,
                user_id INTEGER NOT NULL REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shift_id INTEGER NOT NULL REFERENCES shifts(id),
                table_id INTEGER REFERENCES tables(id),
                order_type TEXT NOT NULL CHECK (order_type IN ('here', 'takeaway')),
                created_at TEXT NOT NULL,
                total REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL CHECK (status IN ('open', 'paid', 'cancelled'))
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL REFERENCES orders(id),
                menu_item_id INTEGER NOT NULL REFERENCES menu_items(id),
                name TEXT NOT NULL,
                modifiers TEXT NOT NULL DEFAULT '',
                quantity INTEGER NOT NULL DEFAULT 1,
                price REAL NOT NULL
            );
            ";
        command.ExecuteNonQuery();
        Seed();
    }

    private static void Seed()
    {
        using var connection = Open();

        var count = new SqliteCommand(
            "SELECT COUNT(*) FROM users", connection);
        var hasUsers = (long)count.ExecuteScalar()! > 0;
        if (hasUsers)
        {
            return;
        }

        var salt = Guid.NewGuid().ToString("N")[..16];
        var hash = AuthService.HashPassword("admin", salt);
        var baristaSalt = Guid.NewGuid().ToString("N")[..16];
        var baristaHash = AuthService.HashPassword("barista", baristaSalt);

        var insert = connection.CreateCommand();
        insert.CommandText = @"
            INSERT INTO users (login, password_hash, salt, full_name, role)
            VALUES ('admin', $hash, $salt, 'Елизаров Максим Вячеславович', 'admin');

            INSERT INTO users (login, password_hash, salt, full_name, role)
            VALUES ('barista', $bhash, $bsalt, 'Разин Константин Евгеньевич', 'barista');

            INSERT INTO menu_items (name, category, price, is_available)
            VALUES ('Эспрессо', 'Кофе', 120, 1),
                   ('Американо', 'Кофе', 140, 1),
                   ('Капучино', 'Кофе', 190, 1),
                   ('Латте', 'Кофе', 210, 1),
                   ('Раф', 'Кофе', 250, 1),
                   ('Чёрный чай', 'Чай', 120, 1),
                   ('Зелёный чай', 'Чай', 130, 1),
                   ('Чизкейк', 'Десерты', 280, 1),
                   ('Круассан', 'Выпечка', 160, 1),
                   ('Булочка с корицей', 'Выпечка', 120, 1);

            INSERT INTO tables (number, seats)
            VALUES (1, 2), (2, 2), (3, 4), (4, 4),
                   (5, 4), (6, 6), (7, 6), (8, 8);
            ";
        insert.Parameters.AddWithValue("$hash", hash);
        insert.Parameters.AddWithValue("$salt", salt);
        insert.Parameters.AddWithValue("$bhash", baristaHash);
        insert.Parameters.AddWithValue("$bsalt", baristaSalt);
        insert.ExecuteNonQuery();
    }
}
