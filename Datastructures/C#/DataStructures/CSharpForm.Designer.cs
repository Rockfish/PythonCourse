namespace DataStructures
{
    partial class CSharpForm
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
            this.components = new System.ComponentModel.Container();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.tssmiSaveJSON = new System.Windows.Forms.ToolStripMenuItem();
            this.tsmiLoadJSON = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.tsmiSaveXML = new System.Windows.Forms.ToolStripMenuItem();
            this.tsmiLoadXML = new System.Windows.Forms.ToolStripMenuItem();
            this.contextMenuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // textBox1
            // 
            this.textBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBox1.ContextMenuStrip = this.contextMenuStrip1;
            this.textBox1.Location = new System.Drawing.Point(12, 12);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBox1.Size = new System.Drawing.Size(761, 475);
            this.textBox1.TabIndex = 3;
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.tssmiSaveJSON,
            this.tsmiLoadJSON,
            this.toolStripSeparator1,
            this.tsmiSaveXML,
            this.tsmiLoadXML});
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(132, 98);
            // 
            // tssmiSaveJSON
            // 
            this.tssmiSaveJSON.Name = "tssmiSaveJSON";
            this.tssmiSaveJSON.Size = new System.Drawing.Size(131, 22);
            this.tssmiSaveJSON.Text = "Save JSON";
            this.tssmiSaveJSON.Click += new System.EventHandler(this.tssmiSaveJSON_Click);
            // 
            // tsmiLoadJSON
            // 
            this.tsmiLoadJSON.Name = "tsmiLoadJSON";
            this.tsmiLoadJSON.Size = new System.Drawing.Size(131, 22);
            this.tsmiLoadJSON.Text = "Load JSON";
            this.tsmiLoadJSON.Click += new System.EventHandler(this.tsmiLoadJSON_Click);
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(128, 6);
            // 
            // tsmiSaveXML
            // 
            this.tsmiSaveXML.Name = "tsmiSaveXML";
            this.tsmiSaveXML.Size = new System.Drawing.Size(131, 22);
            this.tsmiSaveXML.Text = "Save XML";
            this.tsmiSaveXML.Click += new System.EventHandler(this.tsmiSaveXML_Click);
            // 
            // tsmiLoadXML
            // 
            this.tsmiLoadXML.Name = "tsmiLoadXML";
            this.tsmiLoadXML.Size = new System.Drawing.Size(131, 22);
            this.tsmiLoadXML.Text = "Load XML";
            this.tsmiLoadXML.Click += new System.EventHandler(this.tsmiLoadXML_Click);
            // 
            // CSharpForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(785, 499);
            this.ContextMenuStrip = this.contextMenuStrip1;
            this.Controls.Add(this.textBox1);
            this.Name = "CSharpForm";
            this.Text = "Data Structures me C#";
            this.contextMenuStrip1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.ToolStripMenuItem tssmiSaveJSON;
        private System.Windows.Forms.ToolStripMenuItem tsmiLoadJSON;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
        private System.Windows.Forms.ToolStripMenuItem tsmiSaveXML;
        private System.Windows.Forms.ToolStripMenuItem tsmiLoadXML;
    }
}

