<!-- discovery-metadata: cs=0 xaml=1 deps=6 -->
# Practice project context

- Windows Process project using Visual Basic expressions; entry point is `Main.xaml`.
- `Main.xaml` builds three sample mail rows, reads `mail_request.json`, calls local Ollama through HTTP Request (legacy), validates the nested JSON result, and writes `MailClassification.xlsx`.
- Required dependencies are UiPath.System.Activities, UiPath.WebAPI.Activities, and UiPath.Excel.Activities; additional installed packages are listed in `project.json`.
- Runtime prerequisites: Ollama on the Robot machine and model `qwen3:4b` available locally.
- Validate every changed workflow with `uip rpa validate`, then run `uip rpa build`.
