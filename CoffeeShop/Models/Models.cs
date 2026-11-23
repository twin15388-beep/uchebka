namespace CoffeeShop.Models;

public class User
{
    public int Id { get; set; }
    public string Login { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Salt { get; set; } = string.Empty;
    public string FullName { get; set; } = string.Empty;
    public string Role { get; set; } = "barista";
}

public class MenuItem
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Category { get; set; } = "Кофе";
    public decimal Price { get; set; }
    public bool IsAvailable { get; set; } = true;

    public string Availability => IsAvailable ? "да" : "нет";
}

public class CafeTable
{
    public int Id { get; set; }
    public int Number { get; set; }
    public int Seats { get; set; }
}

public class Shift
{
    public int Id { get; set; }
    public DateTime OpenedAt { get; set; }
    public DateTime? ClosedAt { get; set; }
    public int UserId { get; set; }
    public string UserName { get; set; } = string.Empty;
}

public class Order
{
    public int Id { get; set; }
    public int ShiftId { get; set; }
    public int? TableId { get; set; }
    public string OrderType { get; set; } = "here";
    public DateTime CreatedAt { get; set; }
    public decimal Total { get; set; }
    public string Status { get; set; } = "open";
    public List<OrderItem> Items { get; set; } = new();
}

public class OrderItem
{
    public int Id { get; set; }
    public int OrderId { get; set; }
    public int MenuItemId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Modifiers { get; set; } = string.Empty;
    public int Quantity { get; set; } = 1;
    public decimal Price { get; set; }

    public decimal Sum => Price * Quantity;
}
