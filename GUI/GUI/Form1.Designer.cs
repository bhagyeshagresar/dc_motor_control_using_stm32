namespace GUI
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pwmTextBox = new System.Windows.Forms.TextBox();
            this.setDutyCycleLabel = new System.Windows.Forms.Label();
            this.sendPwmBtn = new System.Windows.Forms.Button();
            this.sensorReadingsGrpBox = new System.Windows.Forms.GroupBox();
            this.resetEncoderBtn = new System.Windows.Forms.Button();
            this.EncoderDegsTxtBox = new System.Windows.Forms.TextBox();
            this.readEncoderDegsBtn = new System.Windows.Forms.Button();
            this.encoderCntsTxtBox = new System.Windows.Forms.TextBox();
            this.readEncoderCntsBtn = new System.Windows.Forms.Button();
            this.currentAmpsTxtBox = new System.Windows.Forms.TextBox();
            this.readCurrentAmpsBtn = new System.Windows.Forms.Button();
            this.adcCountsTxtBox = new System.Windows.Forms.TextBox();
            this.readADCCountsBtn = new System.Windows.Forms.Button();
            this.motorControlGrpBox = new System.Windows.Forms.GroupBox();
            this.setPositionGainsGrpBox = new System.Windows.Forms.GroupBox();
            this.goToAngleBtn = new System.Windows.Forms.Button();
            this.positionKdTxtBox = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.setPositionGainsBtn = new System.Windows.Forms.Button();
            this.positionKiTxtBox = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.positionKpTxtBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.setCurrentGainsGrpBox = new System.Windows.Forms.GroupBox();
            this.testCurrentControlBtn = new System.Windows.Forms.Button();
            this.setCurrentGainsBtn = new System.Windows.Forms.Button();
            this.CurrentKiTxtBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.currentKpTxtBox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.iTestPlot = new ScottPlot.WinForms.FormsPlot();
            this.statusLabel = new System.Windows.Forms.Label();
            this.statusTextBox = new System.Windows.Forms.TextBox();
            this.sensorReadingsGrpBox.SuspendLayout();
            this.motorControlGrpBox.SuspendLayout();
            this.setPositionGainsGrpBox.SuspendLayout();
            this.setCurrentGainsGrpBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // pwmTextBox
            // 
            this.pwmTextBox.Location = new System.Drawing.Point(202, 70);
            this.pwmTextBox.Name = "pwmTextBox";
            this.pwmTextBox.Size = new System.Drawing.Size(150, 22);
            this.pwmTextBox.TabIndex = 0;
            this.pwmTextBox.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // setDutyCycleLabel
            // 
            this.setDutyCycleLabel.AutoSize = true;
            this.setDutyCycleLabel.Location = new System.Drawing.Point(16, 41);
            this.setDutyCycleLabel.Name = "setDutyCycleLabel";
            this.setDutyCycleLabel.Size = new System.Drawing.Size(63, 16);
            this.setDutyCycleLabel.TabIndex = 1;
            this.setDutyCycleLabel.Text = "Set PWM";
            // 
            // sendPwmBtn
            // 
            this.sendPwmBtn.Location = new System.Drawing.Point(19, 61);
            this.sendPwmBtn.Name = "sendPwmBtn";
            this.sendPwmBtn.Size = new System.Drawing.Size(101, 31);
            this.sendPwmBtn.TabIndex = 2;
            this.sendPwmBtn.Text = "Send PWM";
            this.sendPwmBtn.UseVisualStyleBackColor = true;
            this.sendPwmBtn.Click += new System.EventHandler(this.sendDutyCycleButtonClick);
            // 
            // sensorReadingsGrpBox
            // 
            this.sensorReadingsGrpBox.Controls.Add(this.resetEncoderBtn);
            this.sensorReadingsGrpBox.Controls.Add(this.EncoderDegsTxtBox);
            this.sensorReadingsGrpBox.Controls.Add(this.readEncoderDegsBtn);
            this.sensorReadingsGrpBox.Controls.Add(this.encoderCntsTxtBox);
            this.sensorReadingsGrpBox.Controls.Add(this.readEncoderCntsBtn);
            this.sensorReadingsGrpBox.Controls.Add(this.currentAmpsTxtBox);
            this.sensorReadingsGrpBox.Controls.Add(this.readCurrentAmpsBtn);
            this.sensorReadingsGrpBox.Controls.Add(this.adcCountsTxtBox);
            this.sensorReadingsGrpBox.Controls.Add(this.readADCCountsBtn);
            this.sensorReadingsGrpBox.Location = new System.Drawing.Point(15, 15);
            this.sensorReadingsGrpBox.Name = "sensorReadingsGrpBox";
            this.sensorReadingsGrpBox.Size = new System.Drawing.Size(368, 277);
            this.sensorReadingsGrpBox.TabIndex = 3;
            this.sensorReadingsGrpBox.TabStop = false;
            this.sensorReadingsGrpBox.Text = "Sensor Readings";
            // 
            // resetEncoderBtn
            // 
            this.resetEncoderBtn.Location = new System.Drawing.Point(22, 234);
            this.resetEncoderBtn.Name = "resetEncoderBtn";
            this.resetEncoderBtn.Size = new System.Drawing.Size(180, 24);
            this.resetEncoderBtn.TabIndex = 12;
            this.resetEncoderBtn.Text = "Reset Encoder";
            this.resetEncoderBtn.UseVisualStyleBackColor = true;
            this.resetEncoderBtn.Click += new System.EventHandler(this.resetEncoderClick);
            // 
            // EncoderDegsTxtBox
            // 
            this.EncoderDegsTxtBox.Location = new System.Drawing.Point(236, 190);
            this.EncoderDegsTxtBox.Name = "EncoderDegsTxtBox";
            this.EncoderDegsTxtBox.ReadOnly = true;
            this.EncoderDegsTxtBox.Size = new System.Drawing.Size(116, 22);
            this.EncoderDegsTxtBox.TabIndex = 11;
            // 
            // readEncoderDegsBtn
            // 
            this.readEncoderDegsBtn.Location = new System.Drawing.Point(22, 188);
            this.readEncoderDegsBtn.Name = "readEncoderDegsBtn";
            this.readEncoderDegsBtn.Size = new System.Drawing.Size(180, 24);
            this.readEncoderDegsBtn.TabIndex = 10;
            this.readEncoderDegsBtn.Text = "Read Encoder (Degrees)";
            this.readEncoderDegsBtn.UseVisualStyleBackColor = true;
            this.readEncoderDegsBtn.Click += new System.EventHandler(this.readEncoderDegreesClick);
            // 
            // encoderCntsTxtBox
            // 
            this.encoderCntsTxtBox.Location = new System.Drawing.Point(236, 141);
            this.encoderCntsTxtBox.Name = "encoderCntsTxtBox";
            this.encoderCntsTxtBox.ReadOnly = true;
            this.encoderCntsTxtBox.Size = new System.Drawing.Size(116, 22);
            this.encoderCntsTxtBox.TabIndex = 9;
            // 
            // readEncoderCntsBtn
            // 
            this.readEncoderCntsBtn.Location = new System.Drawing.Point(22, 139);
            this.readEncoderCntsBtn.Name = "readEncoderCntsBtn";
            this.readEncoderCntsBtn.Size = new System.Drawing.Size(180, 24);
            this.readEncoderCntsBtn.TabIndex = 8;
            this.readEncoderCntsBtn.Text = "Read Encoder (Counts)";
            this.readEncoderCntsBtn.UseVisualStyleBackColor = true;
            this.readEncoderCntsBtn.Click += new System.EventHandler(this.readEncoderCntsClick);
            // 
            // currentAmpsTxtBox
            // 
            this.currentAmpsTxtBox.Location = new System.Drawing.Point(236, 93);
            this.currentAmpsTxtBox.Name = "currentAmpsTxtBox";
            this.currentAmpsTxtBox.ReadOnly = true;
            this.currentAmpsTxtBox.Size = new System.Drawing.Size(116, 22);
            this.currentAmpsTxtBox.TabIndex = 7;
            // 
            // readCurrentAmpsBtn
            // 
            this.readCurrentAmpsBtn.Location = new System.Drawing.Point(22, 91);
            this.readCurrentAmpsBtn.Name = "readCurrentAmpsBtn";
            this.readCurrentAmpsBtn.Size = new System.Drawing.Size(180, 24);
            this.readCurrentAmpsBtn.TabIndex = 6;
            this.readCurrentAmpsBtn.Text = "Read Current (mA)";
            this.readCurrentAmpsBtn.UseVisualStyleBackColor = true;
            this.readCurrentAmpsBtn.Click += new System.EventHandler(this.readCurrentAmpsClick);
            // 
            // adcCountsTxtBox
            // 
            this.adcCountsTxtBox.Location = new System.Drawing.Point(236, 49);
            this.adcCountsTxtBox.Name = "adcCountsTxtBox";
            this.adcCountsTxtBox.ReadOnly = true;
            this.adcCountsTxtBox.Size = new System.Drawing.Size(116, 22);
            this.adcCountsTxtBox.TabIndex = 5;
            // 
            // readADCCountsBtn
            // 
            this.readADCCountsBtn.Location = new System.Drawing.Point(22, 47);
            this.readADCCountsBtn.Name = "readADCCountsBtn";
            this.readADCCountsBtn.Size = new System.Drawing.Size(180, 24);
            this.readADCCountsBtn.TabIndex = 4;
            this.readADCCountsBtn.Text = "Read ADC Counts";
            this.readADCCountsBtn.UseVisualStyleBackColor = true;
            this.readADCCountsBtn.Click += new System.EventHandler(this.readADCCountsClick);
            // 
            // motorControlGrpBox
            // 
            this.motorControlGrpBox.Controls.Add(this.setPositionGainsGrpBox);
            this.motorControlGrpBox.Controls.Add(this.label2);
            this.motorControlGrpBox.Controls.Add(this.setCurrentGainsGrpBox);
            this.motorControlGrpBox.Controls.Add(this.setDutyCycleLabel);
            this.motorControlGrpBox.Controls.Add(this.sendPwmBtn);
            this.motorControlGrpBox.Controls.Add(this.pwmTextBox);
            this.motorControlGrpBox.Location = new System.Drawing.Point(15, 313);
            this.motorControlGrpBox.Name = "motorControlGrpBox";
            this.motorControlGrpBox.Size = new System.Drawing.Size(368, 444);
            this.motorControlGrpBox.TabIndex = 4;
            this.motorControlGrpBox.TabStop = false;
            this.motorControlGrpBox.Text = "Motor Control Settings";
            // 
            // setPositionGainsGrpBox
            // 
            this.setPositionGainsGrpBox.Controls.Add(this.goToAngleBtn);
            this.setPositionGainsGrpBox.Controls.Add(this.positionKdTxtBox);
            this.setPositionGainsGrpBox.Controls.Add(this.label6);
            this.setPositionGainsGrpBox.Controls.Add(this.setPositionGainsBtn);
            this.setPositionGainsGrpBox.Controls.Add(this.positionKiTxtBox);
            this.setPositionGainsGrpBox.Controls.Add(this.label4);
            this.setPositionGainsGrpBox.Controls.Add(this.positionKpTxtBox);
            this.setPositionGainsGrpBox.Controls.Add(this.label5);
            this.setPositionGainsGrpBox.Location = new System.Drawing.Point(6, 268);
            this.setPositionGainsGrpBox.Name = "setPositionGainsGrpBox";
            this.setPositionGainsGrpBox.Size = new System.Drawing.Size(346, 129);
            this.setPositionGainsGrpBox.TabIndex = 10;
            this.setPositionGainsGrpBox.TabStop = false;
            this.setPositionGainsGrpBox.Text = "Set Position Gains";
            // 
            // goToAngleBtn
            // 
            this.goToAngleBtn.Location = new System.Drawing.Point(6, 97);
            this.goToAngleBtn.Name = "goToAngleBtn";
            this.goToAngleBtn.Size = new System.Drawing.Size(139, 26);
            this.goToAngleBtn.TabIndex = 10;
            this.goToAngleBtn.Text = "Go to angle (deg)";
            this.goToAngleBtn.UseVisualStyleBackColor = true;
            // 
            // positionKdTxtBox
            // 
            this.positionKdTxtBox.Location = new System.Drawing.Point(274, 51);
            this.positionKdTxtBox.Name = "positionKdTxtBox";
            this.positionKdTxtBox.Size = new System.Drawing.Size(31, 22);
            this.positionKdTxtBox.TabIndex = 10;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(276, 26);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(23, 16);
            this.label6.TabIndex = 9;
            this.label6.Text = "Kd";
            // 
            // setPositionGainsBtn
            // 
            this.setPositionGainsBtn.Location = new System.Drawing.Point(6, 49);
            this.setPositionGainsBtn.Name = "setPositionGainsBtn";
            this.setPositionGainsBtn.Size = new System.Drawing.Size(101, 26);
            this.setPositionGainsBtn.TabIndex = 4;
            this.setPositionGainsBtn.Text = "Set ";
            this.setPositionGainsBtn.UseVisualStyleBackColor = true;
            // 
            // positionKiTxtBox
            // 
            this.positionKiTxtBox.Location = new System.Drawing.Point(228, 51);
            this.positionKiTxtBox.Name = "positionKiTxtBox";
            this.positionKiTxtBox.Size = new System.Drawing.Size(31, 22);
            this.positionKiTxtBox.TabIndex = 8;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(177, 26);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(23, 16);
            this.label4.TabIndex = 5;
            this.label4.Text = "Kp";
            // 
            // positionKpTxtBox
            // 
            this.positionKpTxtBox.Location = new System.Drawing.Point(180, 51);
            this.positionKpTxtBox.Name = "positionKpTxtBox";
            this.positionKpTxtBox.Size = new System.Drawing.Size(31, 22);
            this.positionKpTxtBox.TabIndex = 7;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(225, 26);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(18, 16);
            this.label5.TabIndex = 6;
            this.label5.Text = "Ki";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(199, 41);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(114, 16);
            this.label2.TabIndex = 10;
            this.label2.Text = "PWM (-100 to 100)";
            // 
            // setCurrentGainsGrpBox
            // 
            this.setCurrentGainsGrpBox.Controls.Add(this.testCurrentControlBtn);
            this.setCurrentGainsGrpBox.Controls.Add(this.setCurrentGainsBtn);
            this.setCurrentGainsGrpBox.Controls.Add(this.CurrentKiTxtBox);
            this.setCurrentGainsGrpBox.Controls.Add(this.label1);
            this.setCurrentGainsGrpBox.Controls.Add(this.currentKpTxtBox);
            this.setCurrentGainsGrpBox.Controls.Add(this.label3);
            this.setCurrentGainsGrpBox.Location = new System.Drawing.Point(6, 110);
            this.setCurrentGainsGrpBox.Name = "setCurrentGainsGrpBox";
            this.setCurrentGainsGrpBox.Size = new System.Drawing.Size(346, 141);
            this.setCurrentGainsGrpBox.TabIndex = 9;
            this.setCurrentGainsGrpBox.TabStop = false;
            this.setCurrentGainsGrpBox.Text = "Set Current Gains";
            // 
            // testCurrentControlBtn
            // 
            this.testCurrentControlBtn.Location = new System.Drawing.Point(6, 80);
            this.testCurrentControlBtn.Name = "testCurrentControlBtn";
            this.testCurrentControlBtn.Size = new System.Drawing.Size(139, 26);
            this.testCurrentControlBtn.TabIndex = 9;
            this.testCurrentControlBtn.Text = "Test Current Control";
            this.testCurrentControlBtn.UseVisualStyleBackColor = true;
            // 
            // setCurrentGainsBtn
            // 
            this.setCurrentGainsBtn.Location = new System.Drawing.Point(6, 39);
            this.setCurrentGainsBtn.Name = "setCurrentGainsBtn";
            this.setCurrentGainsBtn.Size = new System.Drawing.Size(101, 26);
            this.setCurrentGainsBtn.TabIndex = 4;
            this.setCurrentGainsBtn.Text = "Set ";
            this.setCurrentGainsBtn.UseVisualStyleBackColor = true;
            // 
            // CurrentKiTxtBox
            // 
            this.CurrentKiTxtBox.Location = new System.Drawing.Point(228, 43);
            this.CurrentKiTxtBox.Name = "CurrentKiTxtBox";
            this.CurrentKiTxtBox.Size = new System.Drawing.Size(31, 22);
            this.CurrentKiTxtBox.TabIndex = 8;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(177, 18);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(23, 16);
            this.label1.TabIndex = 5;
            this.label1.Text = "Kp";
            // 
            // currentKpTxtBox
            // 
            this.currentKpTxtBox.Location = new System.Drawing.Point(180, 43);
            this.currentKpTxtBox.Name = "currentKpTxtBox";
            this.currentKpTxtBox.Size = new System.Drawing.Size(31, 22);
            this.currentKpTxtBox.TabIndex = 7;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(225, 18);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(18, 16);
            this.label3.TabIndex = 6;
            this.label3.Text = "Ki";
            // 
            // iTestPlot
            // 
            this.iTestPlot.DisplayScale = 0F;
            this.iTestPlot.Location = new System.Drawing.Point(420, 106);
            this.iTestPlot.Name = "iTestPlot";
            this.iTestPlot.Size = new System.Drawing.Size(869, 443);
            this.iTestPlot.TabIndex = 5;
            // 
            // statusLabel
            // 
            this.statusLabel.AutoSize = true;
            this.statusLabel.Location = new System.Drawing.Point(417, 36);
            this.statusLabel.Name = "statusLabel";
            this.statusLabel.Size = new System.Drawing.Size(55, 20);
            this.statusLabel.TabIndex = 6;
            this.statusLabel.Text = "Status";
            // 
            // statusTextBox
            // 
            this.statusTextBox.Location = new System.Drawing.Point(420, 63);
            this.statusTextBox.Name = "statusTextBox";
            this.statusTextBox.Size = new System.Drawing.Size(100, 22);
            this.statusTextBox.TabIndex = 7;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1340, 923);
            this.Controls.Add(this.statusTextBox);
            this.Controls.Add(this.statusLabel);
            this.Controls.Add(this.iTestPlot);
            this.Controls.Add(this.motorControlGrpBox);
            this.Controls.Add(this.sensorReadingsGrpBox);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.sensorReadingsGrpBox.ResumeLayout(false);
            this.sensorReadingsGrpBox.PerformLayout();
            this.motorControlGrpBox.ResumeLayout(false);
            this.motorControlGrpBox.PerformLayout();
            this.setPositionGainsGrpBox.ResumeLayout(false);
            this.setPositionGainsGrpBox.PerformLayout();
            this.setCurrentGainsGrpBox.ResumeLayout(false);
            this.setCurrentGainsGrpBox.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox pwmTextBox;
        private System.Windows.Forms.Label setDutyCycleLabel;
        private System.Windows.Forms.Button sendPwmBtn;
        private System.Windows.Forms.GroupBox sensorReadingsGrpBox;
        private System.Windows.Forms.Button resetEncoderBtn;
        private System.Windows.Forms.TextBox EncoderDegsTxtBox;
        private System.Windows.Forms.Button readEncoderDegsBtn;
        private System.Windows.Forms.TextBox encoderCntsTxtBox;
        private System.Windows.Forms.Button readEncoderCntsBtn;
        private System.Windows.Forms.TextBox currentAmpsTxtBox;
        private System.Windows.Forms.Button readCurrentAmpsBtn;
        private System.Windows.Forms.TextBox adcCountsTxtBox;
        private System.Windows.Forms.Button readADCCountsBtn;
        private System.Windows.Forms.GroupBox motorControlGrpBox;
        private System.Windows.Forms.Button setCurrentGainsBtn;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox CurrentKiTxtBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox currentKpTxtBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.GroupBox setPositionGainsGrpBox;
        private System.Windows.Forms.Button setPositionGainsBtn;
        private System.Windows.Forms.TextBox positionKiTxtBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox positionKpTxtBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox positionKdTxtBox;
        private System.Windows.Forms.GroupBox setCurrentGainsGrpBox;
        private System.Windows.Forms.Button testCurrentControlBtn;
        private System.Windows.Forms.Button goToAngleBtn;
        private ScottPlot.WinForms.FormsPlot iTestPlot;
        private System.Windows.Forms.Label statusLabel;
        private System.Windows.Forms.TextBox statusTextBox;
    }
}

