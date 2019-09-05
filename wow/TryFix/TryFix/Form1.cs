using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace TryFix
{

    public partial class TryFix : Form
    {
        public FixConfig cfg;
        public Dm.dmsoft dm;
        public string configFile;
        public bool isRun = false;

        public TryFix()
        {
            InitializeComponent();
            FixConfig.AutoRegCom("regsvr32 -s dm.dll");

            string cwd = Directory.GetCurrentDirectory();
            configFile = cwd + "\\config.json";

            dm = new Dm.dmsoft();
        }

        private void TryFix_Load(object sender, EventArgs e)
        {
            FixConfig.WriteLog("读取配置文件：" + configFile);
            cfg = FixConfig.loadFromJsonFile(configFile);
            FixConfig.WriteLog("当前配置：" + cfg.dumps());
            initByCfg(cfg);
            setStatus("程序已就绪");
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isRun)
            {
                DialogResult ret = MessageBox.Show("当前正在运行中，确定关闭？", "确定关闭", MessageBoxButtons.OKCancel);
                if (ret == DialogResult.Cancel)
                {
                    e.Cancel = true;
                }
            }

        }

        private void initByCfg(FixConfig cfg)
        {
            fishKeyText.Text = cfg.fishKeyText;
            baitKeyText.Text = cfg.baitKeyText;
            fishSecText.Text = cfg.fishSecText;
            baitSecText.Text = cfg.baitSecText;
            scanCfgText.Text = cfg.scanCfgText;
        }

        public void setStatus(string msg, string tag = "info")
        {
            statusLable.Text = msg;
            FixConfig.WriteLog(msg, tag);
        }

        private void startBtn_Click(object sender, EventArgs e)
        {
            if (isRun)
            {

            }
            if (dm == null)
            {
                setStatus("插件加载失败");
                return;
            }

            isRun = true;
            setStatus("开始运行");
        }
    }

    public class FixConfig
    {
        public string fishKeyText = "1";
        public string baitKeyText = "2";
        public string fishSecText = "30";
        public string baitSecText = "600";
        public string scanCfgText = "30,24,9,7";

        public string dumps()
        {
            return JsonConvert.SerializeObject(this);
        }

        public void readFromJsonObject(JObject jsonObject)
        {
            string _fishKeyText = jsonObject.GetValue("fishKeyText").Value<string>().Trim();
            string _baitKeyText = jsonObject.GetValue("baitKeyText").Value<string>().Trim();
            string _fishSecText = jsonObject.GetValue("fishSecText").Value<string>().Trim();
            string _baitSecText = jsonObject.GetValue("baitSecText").Value<string>().Trim();
            string _scanCfgText = jsonObject.GetValue("scanCfgText").Value<string>();
            if (_fishKeyText != null && _fishKeyText.Length > 0)
            {
                fishKeyText = _fishKeyText;
            }
            if (_baitKeyText != null && _baitKeyText.Length > 0)
            {
                _baitKeyText = _baitKeyText.Trim();
            }

            int iInt;
            if (_fishSecText != null && _fishSecText.Length > 0)
            {
                if (int.TryParse(_fishSecText, out iInt) && iInt > 0 && iInt < 60)
                {
                    fishSecText = _fishSecText;
                }
            }
            if (_baitSecText != null && _baitSecText.Length > 0)
            {
                if (int.TryParse(_baitSecText, out iInt) && iInt > 0 && iInt < 3600)
                {
                    baitSecText = _baitSecText;
                }
            }
            if (_scanCfgText != null && _scanCfgText.Length > 0)
            {
                scanCfgText = _scanCfgText;
            }
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
            string line = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + " [" + tag.ToUpper() + "]" + strLog;
            Console.WriteLine();

            string cwd = Directory.GetCurrentDirectory();
            int pid = Process.GetCurrentProcess().Id;

            string sFilePath = cwd + "\\logs";
            string sFileName = "log_" + DateTime.Now.ToString("yyyy_MM_dd") + "_" + pid + ".log";
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

        public static string AutoRegCom(string strCmd)
        {
            string rInfo;

            try
            {
                Process myProcess = new Process();
                ProcessStartInfo myProcessStartInfo = new ProcessStartInfo("cmd.exe");
                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcess.StartInfo = myProcessStartInfo;
                myProcessStartInfo.Arguments = "/c " + strCmd;
                myProcess.Start();
                StreamReader myStreamReader = myProcess.StandardOutput;
                rInfo = myStreamReader.ReadToEnd();
                myProcess.Close();
                rInfo = strCmd + "\r\n" + rInfo;
                return rInfo;
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
    }
}
