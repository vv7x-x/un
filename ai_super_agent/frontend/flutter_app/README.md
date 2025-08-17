# Flutter Desktop/Web/Mobile UI

Create a Flutter app and add a basic UI that calls the FastAPI backend.

## Quick Start

```bash
flutter create ai_super_agent_flutter
cd ai_super_agent_flutter
flutter run -d linux # or windows, macos, web, android, ios
```

## Minimal Example (lib/main.dart)

```dart
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const apiBase = 'http://127.0.0.1:8000';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Super Agent',
      theme: ThemeData.dark(),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String provider = 'ollama';
  String model = '';
  final promptCtrl = TextEditingController();
  String output = '';

  Future<void> complete() async {
    setState(() => output = 'Running...');
    final resp = await http.post(
      Uri.parse('$apiBase/api/ai/complete'),
      headers: {'content-type': 'application/json'},
      body: jsonEncode({
        'prompt': promptCtrl.text,
        'provider': provider,
        'model': model.isEmpty ? null : model,
      }),
    );
    final data = jsonDecode(resp.body) as Map<String, dynamic>;
    setState(() => output = (data['text'] ?? '').toString());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Super Agent')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(children: [
          Row(children: [
            const Text('Provider'),
            const SizedBox(width: 12),
            DropdownButton<String>(
              value: provider,
              items: const [
                DropdownMenuItem(value: 'ollama', child: Text('ollama')),
                DropdownMenuItem(value: 'openai', child: Text('openai')),
                DropdownMenuItem(value: 'gemini', child: Text('gemini')),
                DropdownMenuItem(value: 'anthropic', child: Text('anthropic')),
              ],
              onChanged: (v) => setState(() => provider = v ?? 'ollama'),
            ),
            const SizedBox(width: 12),
            SizedBox(width: 200, child: TextField(decoration: const InputDecoration(labelText: 'Model'), onChanged: (v) => model = v)),
            const Spacer(),
            ElevatedButton(onPressed: complete, child: const Text('Complete')),
          ]),
          const SizedBox(height: 12),
          Expanded(child: TextField(controller: promptCtrl, maxLines: null, expands: true, decoration: const InputDecoration(labelText: 'Prompt'))),
          const SizedBox(height: 12),
          Expanded(child: Text(output)),
        ]),
      ),
    );
  }
}
```