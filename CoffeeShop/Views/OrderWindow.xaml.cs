using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Controls;
using CoffeeShop.Data;
using CoffeeShop.Models;

namespace CoffeeShop.Views;

public partial class OrderWindow : Window
{
    private readonly User _user;
    private readonly Shift _shift;
    private readonly ObservableCollection<OrderItem> _items = new();

    public OrderWindow(User user)
    {
        InitializeComponent();

        _user = user;
        _shift = ShiftRepository.GetCurrent()
            ?? throw new InvalidOperationException(
                "Смена не открыта. Откройте смену в разделе «Смены».");

        ShiftInfoText.Text =
            $"смена открыта {_shift.OpenedAt:dd.MM.yyyy HH:mm}";

        TableBox.ItemsSource = TableRepository.GetAll();
        TableBox.DisplayMemberPath = "Number";
        TableBox.SelectedValuePath = "Id";
        TableBox.SelectedIndex = 3;

        MenuList.ItemsSource = MenuRepository.GetAll();
        OrderGrid.ItemsSource = _items;
        UpdateTotal();
    }

    private decimal ModifierPrice()
    {
        var sum = 0m;
        if (SizeBox.SelectedIndex == 1) sum += 40;
        if (MilkBox.SelectedIndex > 0) sum += 30;
        if (SyrupBox.SelectedIndex > 0) sum += 20;
        if (CreamCheck.IsChecked == true) sum += 25;
        return sum;
    }

    private string ModifierText()
    {
        var parts = new List<string>();
        if (SizeBox.SelectedIndex == 1) parts.Add("Большой");
        if (MilkBox.SelectedIndex == 1) parts.Add("овсяное молоко");
        if (MilkBox.SelectedIndex == 2) parts.Add("кокосовое молоко");
        if (SyrupBox.SelectedIndex == 1) parts.Add("карамель");
        if (SyrupBox.SelectedIndex == 2) parts.Add("ваниль");
        if (CreamCheck.IsChecked == true) parts.Add("взбитые сливки");
        return parts.Count == 0 ? "—" : string.Join(", ", parts);
    }

    private void AddItem_Click(object sender, RoutedEventArgs e)
    {
        if (MenuList.SelectedItem is not MenuItem item)
        {
            MessageBox.Show("Выберите позицию в меню.",
                "Оформление заказа", MessageBoxButton.OK,
                MessageBoxImage.Warning);
            return;
        }

        if (!int.TryParse(QtyBox.Text, out var quantity) || quantity <= 0)
        {
            MessageBox.Show("Количество должно быть целым числом больше нуля.",
                "Оформление заказа", MessageBoxButton.OK,
                MessageBoxImage.Warning);
            return;
        }

        _items.Add(new OrderItem
        {
            MenuItemId = item.Id,
            Name = item.Name,
            Modifiers = ModifierText(),
            Quantity = quantity,
            Price = item.Price + ModifierPrice()
        });

        UpdateTotal();
    }

    private void DeleteItem_Click(object sender, RoutedEventArgs e)
    {
        if (OrderGrid.SelectedItem is OrderItem item)
        {
            _items.Remove(item);
            UpdateTotal();
        }
    }

    private void UpdateTotal()
    {
        var total = _items.Sum(i => i.Sum);
        TotalText.Text = total.ToString("N2") + " ₽";
    }

    private void SaveOrder_Click(object sender, RoutedEventArgs e) =>
        SaveOrder("open");

    private void PayOrder_Click(object sender, RoutedEventArgs e) =>
        SaveOrder("paid");

    private void SaveOrder(string status)
    {
        if (_items.Count == 0)
        {
            MessageBox.Show("Добавьте хотя бы одну позицию в заказ.",
                "Оформление заказа", MessageBoxButton.OK,
                MessageBoxImage.Warning);
            return;
        }

        if (HereRadio.IsChecked == true && TableBox.SelectedValue is null)
        {
            MessageBox.Show("Выберите столик для заказа на месте.",
                "Оформление заказа", MessageBoxButton.OK,
                MessageBoxImage.Warning);
            return;
        }

        var order = new Order
        {
            ShiftId = _shift.Id,
            TableId = TableBox.SelectedValue as int?,
            OrderType = HereRadio.IsChecked == true ? "here" : "takeaway",
            CreatedAt = DateTime.Now,
            Total = _items.Sum(i => i.Sum),
            Items = _items.ToList()
        };

        OrderRepository.Save(order, status);
        MessageBox.Show(
            status == "paid"
                ? $"Чек закрыт. Сумма {order.Total:N2} ₽."
                : "Заказ сохранён.",
            "Оформление заказа", MessageBoxButton.OK,
            MessageBoxImage.Information);
        Close();
    }
}
