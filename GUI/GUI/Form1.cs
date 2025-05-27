using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;
using ScottPlot;
using ScottPlot.WinForms;


namespace GUI
{
    public partial class Form1 : Form
    {
        private int dutyCycle = 0;
        SerialPort serialPort;
        public Form1()
        {
            InitializeComponent();
            InitializeSerial();
            PlotCurrentTrajectory();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {


        }

        private void InitializeSerial()
        {
            serialPort = new SerialPort();
            serialPort.PortName = "COM9"; // Replace with your port
            serialPort.BaudRate = 115200;
            serialPort.DataBits = 8;
            serialPort.Parity = Parity.None;
            serialPort.StopBits = StopBits.One;
            serialPort.Open();
        }


        private void PlotCurrentTrajectory()
        {
            double frequencyHz = 100;        // 100 Hz square wave
            double amplitude = 200;          // ±200 mA
            double durationMs = 40;          // Show 4 cycles (10 ms per cycle)
            double sampleRate = 10000;       // 0.1 ms resolution

            int pointCount = (int)(durationMs * sampleRate / 1000);
            double[] timeMs = new double[pointCount];
            double[] currentmA = new double[pointCount];

            for (int i = 0; i < pointCount; i++)
            {
                timeMs[i] = i * (1000.0 / sampleRate); // in ms
                double tSec = timeMs[i] / 1000.0;
                currentmA[i] = amplitude * Math.Sign(Math.Sin(2 * Math.PI * frequencyHz * tSec));
            }


            var plt = iTestPlot.Plot;
            plt.Clear();
            plt.Add.Scatter(timeMs, currentmA);
            plt.Title("Reference Current : 100 Hz Square Wave");
            plt.XLabel("Time (ms)");
            plt.YLabel("Current (mA)");

            plt.Axes.SetLimitsX(0, 40); // X axis from 0 ms to 40 ms
            
            iTestPlot.Refresh();

        }


        private void sendDutyCycleButtonClick(object sender, EventArgs e)
        {
            if (int.TryParse(pwmTextBox.Text, out dutyCycle))
            {
                if (serialPort != null && serialPort.IsOpen)
                {
                    byte[] data = BitConverter.GetBytes(dutyCycle); // little endian by default
                    serialPort.Write(data, 0, data.Length);
            
                    // Optional: Show a message or status update
                    MessageBox.Show("Sent: " + dutyCycle);
                }
                else
                {
                    MessageBox.Show("Serial port not open.");
                }
            }
            else
            {
                // Invalid input
                MessageBox.Show("Please enter a valid number.");
            }
        }
    }
    
}
