using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using BTDownloadLib;
using System.IO;
using System.Windows.Forms;

namespace TorrnetGet
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            tbkSaveDir.Text = Directory.GetCurrentDirectory();
        }

        private void btnSelectFile_Click(object sender, RoutedEventArgs e)
        {
            Microsoft.Win32.OpenFileDialog dialog = new Microsoft.Win32.OpenFileDialog();
            dialog.Filter = "文本文件|*.txt";
            dialog.InitialDirectory = Directory.GetCurrentDirectory();
            if (dialog.ShowDialog() == true)
            {
                tbkFileName.Text = dialog.FileName;
                var magnetList = loadMagnetFile(dialog.FileName);
                lbxMagnet.Items.Clear();
                foreach (var item in magnetList)
                {
                    lbxMagnet.Items.Add(item);
                }
                lblState.Content = "载入" + lbxMagnet.Items.Count + "条记录";
            }
        }

        private static List<string> loadMagnetFile(string filename)
        {
            List<string> list = new List<string>();
            using (TextReader reader = File.OpenText(filename))
            {
                string s = reader.ReadLine();
                while (s != null)
                {
                    if(s.StartsWith("magnet:?xt=urn:btih:"))
                    {
                        list.Add(s);
                    }
                    s = reader.ReadLine();
                }
            }
            return list;
        }

        private void btnSelectSaveDir_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog fbd = new FolderBrowserDialog();
            fbd.ShowDialog();
            if (fbd.SelectedPath != string.Empty)
                tbkSaveDir.Text = fbd.SelectedPath;
        }

        private void btnGetTorrnet_Click(object sender, RoutedEventArgs e)
        {
            var obj = new BTServiceInterface();
            foreach (var item in lbxMagnet.Items)
            {
                var url = item.ToString();
                
            }
        }
    }

}
