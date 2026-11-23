using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using CoffeeShop.Data;
using CoffeeShop.Models;

namespace CoffeeShop.Views;

public partial class MenuWindow : Window
{
    private int _selectedId;

    public MenuWindow()
    {
        InitializeComponent();
        Refresh();
    }

    private void Refresh()
    {
        MenuList.ItemsSource = MenuRepository.GetAll();
    }

    private void MenuList_SelectionChanged(
        object sender, System.Windows.Controls.SelectionChangedEventArgs e)
    {
        if (MenuList.SelectedItem is not MenuItem item)
        {
            return;
        }
        _selectedId = item.Id;
        NameBox.Text = item.Name;
        CategoryBox.Text = item.Category;
        PriceBox.Text = item.Price.ToString("0.00");
        AvailableCheck.IsChecked = item.IsAvailable;
    }

    private void Add_Click(object sender, RoutedEventArgs e)
    {
        _selectedId = 0;
        MenuList.SelectedItem = null;
        NameBox.Clear();
        CategoryBox.SelectedIndex = 0;
        PriceBox.Clear();
        AvailableCheck.IsChecked = true;
        NameBox.Focus();
    }

    private void Save_Click(object sender, RoutedEventArgs e)
    {
        var name = NameBox.Text.Trim();
        var category = (CategoryBox.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "";
        var priceText = PriceBox.Text.Trim().Replace(",", ".");

        if (name.Length < 2)
        {
            MessageBox.Show("Введите наименование позиции.",
                "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        if (!decimal.TryParse(priceText, NumberStyles.Number,
                CultureInfo.InvariantCulture, out var price) || price <= 0)
        {
            MessageBox.Show("Цена должна быть положительным числом.",
                "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        MenuRepository.Save(new MenuItem
        {
            Id = _selectedId,
            Name = name,
            Category = category,
            Price = price,
            IsAvailable = AvailableCheck.IsChecked == true
        });

        MessageBox.Show("Данные сохранены.", "Меню",
            MessageBoxButton.OK, MessageBoxImage.Information);
        Refresh();
    }

    private void Delete_Click(object sender, RoutedEventArgs e)
    {
        if (_selectedId == 0)
        {
            MessageBox.Show("Выберите позицию для удаления.",
                "Меню", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        var answer = MessageBox.Show("Удалить выбранную позицию?",
            "Подтверждение", MessageBoxButton.YesNo, MessageBoxImage.Question);
        if (answer != MessageBoxResult.Yes)
        {
            return;
        }

        MenuRepository.Delete(_selectedId);
        Add_Click(sender, e);
        Refresh();
    }
}
