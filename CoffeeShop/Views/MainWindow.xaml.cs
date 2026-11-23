using System.Windows;
using CoffeeShop.Data;
using CoffeeShop.Models;

namespace CoffeeShop.Views;

public partial class MainWindow : Window
{
    private readonly User _user;

    public MainWindow(User user)
    {
        InitializeComponent();
        _user = user;
        UserNameText.Text = user.FullName;
        UserRoleText.Text = user.Role == "admin"
            ? "роль: администратор"
            : "роль: бариста";

        // Разграничение прав: бариста не управляет меню и отчётами
        var isAdmin = user.Role == "admin";
        MenuButton.Visibility = isAdmin
            ? Visibility.Visible
            : Visibility.Collapsed;
        ReportsButton.Visibility = isAdmin
            ? Visibility.Visible
            : Visibility.Collapsed;

        RefreshStatus();
    }

    private void RefreshStatus()
    {
        var shift = ShiftRepository.GetCurrent();
        StatusText.Text = shift is null
            ? "Смена не открыта"
            : $"Смена открыта: {shift.OpenedAt:dd.MM.yyyy HH:mm} · " +
              $"бариста: {shift.UserName}";
    }

    private void Orders_Click(object sender, RoutedEventArgs e)
    {
        if (ShiftRepository.GetCurrent() is null)
        {
            MessageBox.Show(
                "Смена не открыта. Откройте смену в разделе «Смены».",
                "Оформление заказа", MessageBoxButton.OK,
                MessageBoxImage.Warning);
            return;
        }

        new OrderWindow(_user).ShowDialog();
    }

    private void Menu_Click(object sender, RoutedEventArgs e) =>
        new MenuWindow().ShowDialog();

    private void Tables_Click(object sender, RoutedEventArgs e) =>
        MessageBox.Show("В зале 8 столиков: №1–№2 (2 места), №3–№6 (4 места), " +
                        "№7–№8 (6–8 мест).",
            "Столики", MessageBoxButton.OK, MessageBoxImage.Information);

    private void Shifts_Click(object sender, RoutedEventArgs e)
    {
        new ShiftWindow(_user).ShowDialog();
        RefreshStatus();
    }

    private void Reports_Click(object sender, RoutedEventArgs e) =>
        new ReportWindow().ShowDialog();

    private void Exit_Click(object sender, RoutedEventArgs e) =>
        Application.Current.Shutdown();
}
