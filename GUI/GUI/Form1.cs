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
