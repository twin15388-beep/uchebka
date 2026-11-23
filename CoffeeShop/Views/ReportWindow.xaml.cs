using System.Data;
using System.Windows;
using CoffeeShop.Services;

namespace CoffeeShop.Views;

public partial class ReportWindow : Window
{
    public ReportWindow()
    {
        InitializeComponent();
        FromPicker.SelectedDate = DateTime.Today;
        ToPicker.SelectedDate = DateTime.Today;
    }

    private void Generate_Click(object sender, RoutedEventArgs e)
    {
        var from = FromPicker.SelectedDate ?? DateTime.Today;
        var to = ToPicker.SelectedDate ?? DateTime.Today;
        var table = new DataTable();

        switch (ReportTypeBox.SelectedIndex)
        {
            case 0:
                BuildRevenueReport(table, from, to);
                break;
            case 1:
                BuildCategoryReport(table, from, to);
                break;
            default:
                BuildPopularReport(table);
                break;
        }

        ReportGrid.ItemsSource = table.DefaultView;
    }

    private static void BuildRevenueReport(
        DataTable table, DateTime from, DateTime to)
    {
        table.Columns.Add("Показатель");
        table.Columns.Add("Значение");

        var revenue = ReportService.GetRevenue(from, to);
        var checks = ReportService.GetChecksCount(from, to);

        table.Rows.Add("Выручка, ₽", revenue.ToString("N2"));
        table.Rows.Add("Количество чеков", checks);
        table.Rows.Add("Средний чек, ₽",
            checks == 0 ? 0.ToString("N2")
                        : (revenue / checks).ToString("N2"));
    }

    private static void BuildCategoryReport(
        DataTable table, DateTime from, DateTime to)
    {
        table.Columns.Add("Категория");
        table.Columns.Add("Количество");
        table.Columns.Add("Сумма, ₽");

        foreach (var row in ReportService.GetSalesByCategory(from, to))
        {
            table.Rows.Add(row.Name, row.Quantity,
                row.Sum.ToString("N2"));
        }
    }

    private static void BuildPopularReport(DataTable table)
    {
        table.Columns.Add("Позиция");
        table.Columns.Add("Продано, шт.");
        table.Columns.Add("Сумма, ₽");

        foreach (var row in ReportService.GetPopularItems())
        {
            table.Rows.Add(row.Name, row.Quantity,
                row.Sum.ToString("N2"));
        }
    }
}
