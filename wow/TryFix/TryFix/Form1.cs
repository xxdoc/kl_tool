using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Windows.Forms;

namespace TryFix
{


    public partial class TryFix : Form
    {
        public FixConfig cfg;

        public TryFix()
        {
            InitializeComponent();
        }

        private void TryFix_Load(object sender, EventArgs e)
        {
            string cwd = Directory.GetCurrentDirectory();
            string configFile = cwd + "\\config.json";
            cfg = FixConfig.loadFromJsonFile(configFile);
        }

        private void initByCfg(FixConfig cfg)
        {
            fishKeyText.Text = cfg.fishKeyText;
            baitKeyText.Text = cfg.baitKeyText;
            fishSecText.Text = cfg.fishSecText;
            baitSecText.Text = cfg.baitSecText;

        }

    }

    public class FixConfig
    {
        public string fishKeyText = "1";
        public string baitKeyText = "2";
        public string fishSecText = "30";
        public string baitSecText = "600";
        public string scanCfgText = "30,24,9,7";

        public void readFromJsonObject(JObject jsonObject)
        {

        }

        public static FixConfig loadFromJsonFile(string filePath)
        {
            FixConfig cfg = new FixConfig();
            if (File.Exists(filePath))
            {
                StreamReader file = null;
                try
                {
                    file = File.OpenText(filePath);
                    JsonTextReader reader = new JsonTextReader(file);
                    JObject jsonObject = (JObject)JToken.ReadFrom(reader);
                    cfg.readFromJsonObject(jsonObject);
                }
                catch (Exception ex)
                {
                    string log_msg = "read config error:" + ex.Message;
                    WriteLog(log_msg, "error");
                }
                finally
                {
                    if (file != null)
                    {
                        file.Close();
                    }
                }
            }
            dumpToJsonFile(filePath, cfg);
            return cfg;
        }

        public static void dumpToJsonFile(string filePath, FixConfig cfg)
        {
            FileStream fs = new FileStream(filePath, FileMode.Create, FileAccess.Write);
            string jsonStr = JsonConvert.SerializeObject(cfg);
            StreamWriter sw = new StreamWriter(fs);
            sw.WriteLine(jsonStr);
            sw.Close();
            fs.Close();
        }

        public static void WriteLog(string strLog, string tag = "info")
        {
            string line = DateTime.Now.ToString("yyyy-MM-dd HH-mm-ss") + " [" + tag.ToUpper() + "]" + strLog;
            Console.WriteLine();

            string cwd = Directory.GetCurrentDirectory();

            string sFilePath = cwd + "\\logs";
            string sFileName = "log_" + DateTime.Now.ToString("yyyyMMdd") + ".log";
            sFileName = sFilePath + "\\" + sFileName; //文件的绝对路径
            if (!Directory.Exists(sFilePath))
            {
                Directory.CreateDirectory(sFilePath);
            }

            FileStream fs;
            StreamWriter sw;
            if (File.Exists(sFileName))
            //验证文件是否存在，有则追加，无则创建
            {
                fs = new FileStream(sFileName, FileMode.Append, FileAccess.Write);
            }
            else
            {
                fs = new FileStream(sFileName, FileMode.Create, FileAccess.Write);
            }
            sw = new StreamWriter(fs);
            sw.WriteLine(line);
            sw.Close();
            fs.Close();
        }
    }
}
