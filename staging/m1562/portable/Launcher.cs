using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

internal static class Launcher
{
    [STAThread]
    private static void Main(string[] args)
    {
        var folder = AppDomain.CurrentDomain.BaseDirectory;
        var runtime = Path.Combine(folder, "App");
        var ready = Path.Combine(Path.GetTempPath(), "Gedangan-" + Guid.NewGuid().ToString("N") + ".port");
        var output = Path.Combine(runtime, "portable-launch.log");
        bool openBrowser = Array.IndexOf(args, "--no-browser") < 0;
        string readyCopy = args.Length == 2 && !openBrowser ? args[1] : null;
        Application.EnableVisualStyles();
        try
        {
            var start = new ProcessStartInfo(Path.Combine(runtime, "Python", "python.exe"),
                "-I -B -u \"" + Path.Combine(runtime, "host.py") + "\" \"" + ready + "\"");
            start.WorkingDirectory = runtime;
            start.UseShellExecute = false;
            start.CreateNoWindow = true;
            start.RedirectStandardError = true;
            start.RedirectStandardOutput = true;
            using (var instance = new System.Threading.Mutex(false, "Gedangan1562-" + MutexKey(folder)))
            {
                bool owned;
                try { owned = instance.WaitOne(0); }
                catch (System.Threading.AbandonedMutexException) { owned = true; }
                if (!owned)
                {
                    MessageBox.Show("Simulator sudah berjalan dari folder ini.", "Gedangan M15.6.2");
                    return;
                }
                using (var log = TextWriter.Synchronized(new StreamWriter(output, false) { AutoFlush = true }))
                using (var server = new Process { StartInfo = start })
                {
                    server.ErrorDataReceived += (s, e) => { if (e.Data != null) log.WriteLine(e.Data); };
                    server.OutputDataReceived += (s, e) => { if (e.Data != null) log.WriteLine(e.Data); };
                    server.Start();
                    server.BeginErrorReadLine();
                    server.BeginOutputReadLine();
                    try { RunWindow(server, ready, readyCopy, openBrowser, output); }
                    finally
                    {
                        if (!server.HasExited)
                        {
                            var stop = new ProcessStartInfo(Path.Combine(Environment.SystemDirectory, "taskkill.exe"),
                                "/PID " + server.Id + " /T /F");
                            stop.UseShellExecute = false;
                            stop.CreateNoWindow = true;
                            using (var killer = Process.Start(stop)) killer.WaitForExit(5000);
                        }
                        server.WaitForExit();
                    }
                }
                instance.ReleaseMutex();
            }
        }
        catch (Exception error)
        {
            MessageBox.Show(error.Message + "\n\nLog: " + output, "Gedangan M15.6.2", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally { if (File.Exists(ready)) File.Delete(ready); }
    }

    private static string MutexKey(string folder)
    {
        using (var sha = System.Security.Cryptography.SHA256.Create())
            return BitConverter.ToString(sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(folder.ToUpperInvariant())));
    }

    private static void RunWindow(Process server, string ready, string readyCopy, bool openBrowser, string log)
    {
        using (var window = new Form { Text = "Gedangan Traffic Simulator M15.6.2", Width = 470, Height = 210,
            StartPosition = FormStartPosition.CenterScreen, FormBorderStyle = FormBorderStyle.FixedDialog, MaximizeBox = false })
        using (var timer = new Timer { Interval = 200 })
        {
            var status = new Label { Left = 18, Top = 18, Width = 420, Height = 48, Text = "Memulai simulator lokal..." };
            var open = new Button { Left = 18, Top = 78, Width = 190, Height = 34, Text = "Buka Simulator", Enabled = false };
            var stop = new Button { Left = 220, Top = 78, Width = 190, Height = 34, Text = "Tutup Simulator" };
            var note = new Label { Left = 18, Top = 124, Width = 420, Text = "Biarkan jendela ini terbuka selama simulasi." };
            window.Controls.AddRange(new Control[] { status, open, stop, note });
            string url = null;
            var launchTime = DateTime.UtcNow;
            Action browse = () =>
            {
                try { Process.Start(new ProcessStartInfo(url) { UseShellExecute = true }); }
                catch { MessageBox.Show("Buka alamat ini di Chrome atau Edge:\n" + url); }
            };
            open.Click += (s, e) => browse();
            stop.Click += (s, e) => window.Close();
            timer.Tick += (s, e) =>
            {
                if (server.HasExited || (url == null && (DateTime.UtcNow - launchTime).TotalSeconds > 30))
                {
                    timer.Stop();
                    status.Text = "Simulator gagal berjalan. Periksa " + Path.GetFileName(log) + " dalam folder App.";
                    open.Enabled = false;
                    return;
                }
                if (url != null || !File.Exists(ready)) return;
                int port;
                if (!int.TryParse(File.ReadAllText(ready), out port) || port < 1 || port > 65535) return;
                url = "http://127.0.0.1:" + port + "/";
                status.Text = "Simulator berjalan di " + url;
                open.Enabled = true;
                if (readyCopy != null) File.WriteAllText(readyCopy, url);
                if (openBrowser) browse();
            };
            timer.Start();
            Application.Run(window);
        }
    }
}
