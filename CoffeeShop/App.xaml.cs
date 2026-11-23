using System.Windows;
using CoffeeShop.Data;

namespace CoffeeShop;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        Database.Initialize();
        base.OnStartup(e);
    }
}
