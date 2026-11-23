using System.Windows;
using CoffeeShop.Services;

namespace CoffeeShop.Views;

public partial class AuthWindow : Window
{
    private int _attempts;

    public AuthWindow()
    {
        InitializeComponent();
        LoginBox.Focus();
    }

    private void Login_Click(object sender, RoutedEventArgs e)
    {
        var login = LoginBox.Text.Trim();
        var password = PasswordBox.Password;

        if (login.Length == 0 || password.Length == 0)
        {
            MessageBox.Show("Введите логин и пароль.", "Кофейня «Зёрнышко»",
                MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        var user = AuthService.Authenticate(login, password);
        if (user is null)
        {
            _attempts++;
            MessageBox.Show("Неверный логин или пароль.", "Ошибка входа",
                MessageBoxButton.OK, MessageBoxImage.Error);
            PasswordBox.Clear();
            PasswordBox.Focus();
            return;
        }

        var main = new MainWindow(user);
        main.Show();
        Close();
    }

    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        Application.Current.Shutdown();
    }
}
