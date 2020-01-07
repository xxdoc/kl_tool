namespace TryFix
{
    partial class TryFix
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.fishKey = new System.Windows.Forms.Label();
            this.fishKeyText = new System.Windows.Forms.TextBox();
            this.baitKey = new System.Windows.Forms.Label();
            this.baitKeyText = new System.Windows.Forms.TextBox();
            this.fishSec = new System.Windows.Forms.Label();
            this.fishSecText = new System.Windows.Forms.TextBox();
            this.baitSec = new System.Windows.Forms.Label();
            this.scanCfg = new System.Windows.Forms.Label();
            this.baitSecText = new System.Windows.Forms.TextBox();
            this.scanCfgText = new System.Windows.Forms.TextBox();
            this.startBtn = new System.Windows.Forms.Button();
            this.stopBtn = new System.Windows.Forms.Button();
            this.statusLable = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // fishKey
            // 
            this.fishKey.AutoSize = true;
            this.fishKey.Location = new System.Drawing.Point(20, 25);
            this.fishKey.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.fishKey.Name = "fishKey";
            this.fishKey.Size = new System.Drawing.Size(82, 15);
            this.fishKey.TabIndex = 0;
            this.fishKey.Text = "钓鱼按键：";
            // 
            // fishKeyText
            // 
            this.fishKeyText.Location = new System.Drawing.Point(117, 16);
            this.fishKeyText.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.fishKeyText.Name = "fishKeyText";
            this.fishKeyText.Size = new System.Drawing.Size(132, 25);
            this.fishKeyText.TabIndex = 3;
            // 
            // baitKey
            // 
            this.baitKey.AutoSize = true;
            this.baitKey.Location = new System.Drawing.Point(20, 64);
            this.baitKey.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.baitKey.Name = "baitKey";
            this.baitKey.Size = new System.Drawing.Size(82, 15);
            this.baitKey.TabIndex = 0;
            this.baitKey.Text = "鱼饵按键：";
            // 
            // baitKeyText
            // 
            this.baitKeyText.Location = new System.Drawing.Point(117, 56);
            this.baitKeyText.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.baitKeyText.Name = "baitKeyText";
            this.baitKeyText.Size = new System.Drawing.Size(132, 25);
            this.baitKeyText.TabIndex = 4;
            // 
            // fishSec
            // 
            this.fishSec.AutoSize = true;
            this.fishSec.Location = new System.Drawing.Point(20, 102);
            this.fishSec.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.fishSec.Name = "fishSec";
            this.fishSec.Size = new System.Drawing.Size(82, 15);
            this.fishSec.TabIndex = 0;
            this.fishSec.Text = "钓鱼周期：";
            // 
            // fishSecText
            // 
            this.fishSecText.Location = new System.Drawing.Point(117, 96);
            this.fishSecText.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.fishSecText.Name = "fishSecText";
            this.fishSecText.Size = new System.Drawing.Size(132, 25);
            this.fishSecText.TabIndex = 5;
            // 
            // baitSec
            // 
            this.baitSec.AutoSize = true;
            this.baitSec.Location = new System.Drawing.Point(20, 141);
            this.baitSec.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.baitSec.Name = "baitSec";
            this.baitSec.Size = new System.Drawing.Size(82, 15);
            this.baitSec.TabIndex = 0;
            this.baitSec.Text = "鱼饵周期：";
            // 
            // scanCfg
            // 
            this.scanCfg.AutoSize = true;
            this.scanCfg.Location = new System.Drawing.Point(20, 180);
            this.scanCfg.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.scanCfg.Name = "scanCfg";
            this.scanCfg.Size = new System.Drawing.Size(82, 15);
            this.scanCfg.TabIndex = 0;
            this.scanCfg.Text = "扫描参数：";
            // 
            // baitSecText
            // 
            this.baitSecText.Location = new System.Drawing.Point(117, 136);
            this.baitSecText.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.baitSecText.Name = "baitSecText";
            this.baitSecText.Size = new System.Drawing.Size(132, 25);
            this.baitSecText.TabIndex = 6;
            // 
            // scanCfgText
            // 
            this.scanCfgText.Location = new System.Drawing.Point(117, 176);
            this.scanCfgText.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.scanCfgText.Name = "scanCfgText";
            this.scanCfgText.Size = new System.Drawing.Size(132, 25);
            this.scanCfgText.TabIndex = 7;
            // 
            // startBtn
            // 
            this.startBtn.Location = new System.Drawing.Point(23, 222);
            this.startBtn.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.startBtn.Name = "startBtn";
            this.startBtn.Size = new System.Drawing.Size(100, 29);
            this.startBtn.TabIndex = 1;
            this.startBtn.Text = "开始";
            this.startBtn.UseVisualStyleBackColor = true;
            this.startBtn.Click += new System.EventHandler(this.startBtn_Click);
            // 
            // stopBtn
            // 
            this.stopBtn.Location = new System.Drawing.Point(151, 222);
            this.stopBtn.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.stopBtn.Name = "stopBtn";
            this.stopBtn.Size = new System.Drawing.Size(100, 29);
            this.stopBtn.TabIndex = 2;
            this.stopBtn.Text = "停止";
            this.stopBtn.UseVisualStyleBackColor = true;
            // 
            // statusLable
            // 
            this.statusLable.AutoSize = true;
            this.statusLable.Location = new System.Drawing.Point(-3, 301);
            this.statusLable.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.statusLable.Name = "statusLable";
            this.statusLable.Size = new System.Drawing.Size(82, 15);
            this.statusLable.TabIndex = 0;
            this.statusLable.Text = "程序已就绪";
            // 
            // TryFix
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(287, 328);
            this.Controls.Add(this.statusLable);
            this.Controls.Add(this.stopBtn);
            this.Controls.Add(this.startBtn);
            this.Controls.Add(this.scanCfgText);
            this.Controls.Add(this.baitSecText);
            this.Controls.Add(this.scanCfg);
            this.Controls.Add(this.baitSec);
            this.Controls.Add(this.fishSecText);
            this.Controls.Add(this.fishSec);
            this.Controls.Add(this.baitKeyText);
            this.Controls.Add(this.baitKey);
            this.Controls.Add(this.fishKeyText);
            this.Controls.Add(this.fishKey);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.MaximizeBox = false;
            this.Name = "TryFix";
            this.Text = "TryFix";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.TryFix_FormClosing);
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.TryFix_FormClosed);
            this.Load += new System.EventHandler(this.TryFix_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label fishKey;
        private System.Windows.Forms.TextBox fishKeyText;
        private System.Windows.Forms.Label baitKey;
        private System.Windows.Forms.TextBox baitKeyText;
        private System.Windows.Forms.Label fishSec;
        private System.Windows.Forms.TextBox fishSecText;
        private System.Windows.Forms.Label baitSec;
        private System.Windows.Forms.Label scanCfg;
        private System.Windows.Forms.TextBox baitSecText;
        private System.Windows.Forms.TextBox scanCfgText;
        private System.Windows.Forms.Button startBtn;
        private System.Windows.Forms.Button stopBtn;
        private System.Windows.Forms.Label statusLable;
    }
}

