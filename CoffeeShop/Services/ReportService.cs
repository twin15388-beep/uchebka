namespace CoffeeShop.Services;

public record SalesRow(string Name, int Quantity, decimal Sum);

public static class ReportService
{
    public static decimal GetRevenue(DateTime from, DateTime to)
    {
        using var connection = Data.Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT COALESCE(SUM(o.total), 0)
            FROM orders o JOIN shifts s ON s.id = o.shift_id
            WHERE o.status = 'paid'
              AND s.opened_at >= $from AND s.opened_at <= $to;
            ";
        command.Parameters.AddWithValue("$from",
            from.ToString("yyyy-MM-dd HH:mm:ss"));
        command.Parameters.AddWithValue("$to",
            to.ToString("yyyy-MM-dd HH:mm:ss"));
        return Convert.ToDecimal(command.ExecuteScalar());
    }

    public static int GetChecksCount(DateTime from, DateTime to)
    {
        using var connection = Data.Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT COUNT(*) FROM orders o
            JOIN shifts s ON s.id = o.shift_id
            WHERE o.status = 'paid'
              AND s.opened_at >= $from AND s.opened_at <= $to;
            ";
        command.Parameters.AddWithValue("$from",
            from.ToString("yyyy-MM-dd HH:mm:ss"));
        command.Parameters.AddWithValue("$to",
            to.ToString("yyyy-MM-dd HH:mm:ss"));
        return Convert.ToInt32(command.ExecuteScalar());
    }

    public static List<SalesRow> GetPopularItems(int top = 5)
    {
        using var connection = Data.Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT i.name, SUM(i.quantity), SUM(i.price * i.quantity)
            FROM order_items i JOIN orders o ON o.id = i.order_id
            WHERE o.status = 'paid'
            GROUP BY i.name
            ORDER BY SUM(i.quantity) DESC LIMIT $top;
            ";
        command.Parameters.AddWithValue("$top", top);
        var rows = new List<SalesRow>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            rows.Add(new SalesRow(
                reader.GetString(0),
                reader.GetInt32(1),
                reader.GetDecimal(2)));
        }
        return rows;
    }

    public static List<SalesRow> GetSalesByCategory(DateTime from, DateTime to)
    {
        using var connection = Data.Database.Open();
        var command = connection.CreateCommand();
        command.CommandText = @"
            SELECT m.category, SUM(i.quantity), SUM(i.price * i.quantity)
            FROM order_items i
            JOIN menu_items m ON m.id = i.menu_item_id
            JOIN orders o ON o.id = i.order_id
            JOIN shifts s ON s.id = o.shift_id
            WHERE o.status = 'paid'
              AND s.opened_at >= $from AND s.opened_at <= $to
            GROUP BY m.category
            ORDER BY SUM(i.price * i.quantity) DESC;
            ";
        command.Parameters.AddWithValue("$from",
            from.ToString("yyyy-MM-dd HH:mm:ss"));
        command.Parameters.AddWithValue("$to",
            to.ToString("yyyy-MM-dd HH:mm:ss"));
        var rows = new List<SalesRow>();
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            rows.Add(new SalesRow(
                reader.GetString(0),
                reader.GetInt32(1),
                reader.GetDecimal(2)));
        }
        return rows;
    }
}
