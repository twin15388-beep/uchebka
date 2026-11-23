using System.Windows;
using CoffeeShop.Data;
using CoffeeShop.Models;

namespace CoffeeShop.Views;

public partial class ShiftWindow : Window
{
    private readonly User _user;

    public ShiftWindow(User user)
    {
        InitializeComponent();
        _user = user;
        Refresh();
    }

    private void Refresh()
    {
        var shift = ShiftRepository.GetCurrent();
        if (shift is null)
        {
            ShiftStatusText.Text = "Смена не открыта";
            ShiftInfoText.Text = "Откройте смену перед началом работы";
            RevenueText.Text = "0,00 ₽";
            ChecksText.Text = "0";
            OpenShiftButton.IsEnabled = true;
            CloseShiftButton.IsEnabled = false;
        }
        else
        {
            ShiftStatusText.Text = "Смена открыта";
            ShiftInfoText.Text =
                $"Открыта {shift.OpenedAt:dd.MM.yyyy HH:mm} · бариста: {shift.UserName}";
            RevenueText.Text =
                ShiftRepository.GetRevenue(shift.Id).ToString("N2") + " ₽";
            ChecksText.Text = OrderRepository.GetByShift(shift.Id)
                .Count(o => o.Status == "paid").ToString();
            OpenShiftButton.IsEnabled = false;
            CloseShiftButton.IsEnabled = true;
        }

        ShiftList.ItemsSource = ShiftRepository.GetClosed()
            .Select(s => new
            {
                OpenedAt = s.OpenedAt.ToString("dd.MM.yyyy HH:mm"),
                s.UserName,
                Revenue = ShiftRepository.GetRevenue(s.Id).ToString("N2")
            })
            .ToList();
    }

    private void OpenShift_Click(object sender, RoutedEventArgs e)
    {
        ShiftRepository.Open(_user.Id);
        Refresh();
    }

    private void CloseShift_Click(object sender, RoutedEventArgs e)
    {
        var shift = ShiftRepository.GetCurrent();
        if (shift is null)
        {
            return;
        }

        var revenue = ShiftRepository.GetRevenue(shift.Id);
        var answer = MessageBox.Show(
            $"Закрыть смену? Выручка за смену: {revenue:N2} ₽.",
            "Закрытие смены", MessageBoxButton.YesNo,
            MessageBoxImage.Question);
        if (answer != MessageBoxResult.Yes)
        {
            return;
        }

        ShiftRepository.Close(shift.Id);
        Refresh();
    }
}
