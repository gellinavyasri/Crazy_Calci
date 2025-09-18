import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:math' as math;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sarcastic Math Genius',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        fontFamily: 'Comic Sans MS',
      ),
      home: CalculatorPage(),
    );
  }
}

class CalculatorPage extends StatefulWidget {
  @override
  _CalculatorPageState createState() => _CalculatorPageState();
}

class _CalculatorPageState extends State<CalculatorPage> with TickerProviderStateMixin {
  final TextEditingController aController = TextEditingController();
  final TextEditingController bController = TextEditingController();
  String result = "🤖 Ready to do math that even a potato could handle!";
  String mood = "😎";
  late AnimationController _shakeController;
  late Animation<double> _shakeAnimation;
  
  final List<String> waitingMessages = [
    "🧠 Calculating with my superior AI brain...",
    "🤯 Hold on, doing rocket science here...",
    "🔮 Consulting the math spirits...",
    "🎭 Pretending this is difficult...",
    "🦾 Flexing my computational muscles...",
    "☕ Taking a coffee break... just kidding!",
  ];

  @override
  void initState() {
    super.initState();
    _shakeController = AnimationController(
      duration: Duration(milliseconds: 500),
      vsync: this,
    );
    _shakeAnimation = Tween<double>(begin: 0, end: 10).animate(
      CurvedAnimation(parent: _shakeController, curve: Curves.elasticIn),
    );
  }

  @override
  void dispose() {
    _shakeController.dispose();
    super.dispose();
  }

  Future<void> calculate(String operation) async {
    final a = int.tryParse(aController.text) ?? 0;
    final b = int.tryParse(bController.text) ?? 0;

    // Show random waiting message
    final randomMessage = waitingMessages[math.Random().nextInt(waitingMessages.length)];
    setState(() {
      result = randomMessage;
      mood = "🤔";
    });

    // Add dramatic pause
    await Future.delayed(Duration(milliseconds: 800 + math.Random().nextInt(1200)));

    final url = Uri.parse("http://192.168.29.174:5000/calculate");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"a": a, "b": b, "operation": operation}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final calculatedResult = data['result'];
      final funnyMessage = data['funny_message'] ?? _generateLocalFunnyMessage(a, b, operation, calculatedResult);
      final serverMood = data['mood'] ?? _generateMood(calculatedResult);
      
      setState(() {
        result = "$funnyMessage\n\n📊 Answer: $calculatedResult";
        mood = serverMood;
      });
      
      // Shake animation for dramatic effect
      _shakeController.forward().then((_) => _shakeController.reverse());
      
    } else {
      setState(() {
        result = "💥 ERROR! My circuits are having a meltdown!\n${response.body}";
        mood = "😵";
      });
    }
  }

  String _generateLocalFunnyMessage(int a, int b, String operation, dynamic result) {
    final messages = {
      'add': [
        "🎉 Wow! You discovered that $a + $b = $result! Nobel Prize incoming!",
        "🧮 Even my calculator from 1985 could do this, but sure...",
        "🎪 *drum roll* The crowd goes wild for basic addition!",
        "🤓 Fun fact: You just performed the same operation cavemen did!",
      ],
      'multiply': [
        "⚡ Multiplication magic! $a × $b = $result (I'm basically Einstein now)",
        "🚀 Houston, we have... basic multiplication!",
        "🎭 And for my next trick, I'll make your mind... slightly less confused!",
        "🦸 With great power (math) comes great responsibility!",
      ],
      'divide': [
        "🔪 Division complete! $a ÷ $b = $result (No numbers were harmed)",
        "⚖️ Justice is served... mathematically!",
        "🎯 Bullseye! Another division conquered!",
      ],
      'subtract': [
        "➖ Subtraction success! $a - $b = $result (Math anxiety: defeated)",
        "🎢 We went down from $a to $result. What a ride!",
        "🔍 Elementary, my dear Watson! It's $result!",
      ],
    };
    
    final operationMessages = messages[operation] ?? ["🤖 Math happened!"];
    return operationMessages[math.Random().nextInt(operationMessages.length)];
  }

  String _generateMood(dynamic result) {
    final num = double.tryParse(result.toString()) ?? 0;
    if (num == 0) return "😐";
    if (num < 0) return "😬";
    if (num > 100) return "🤯";
    if (num == 42) return "🤖"; // Hitchhiker's reference
    if (num % 2 == 0) return "😊";
    return "🤪";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Text("🧠 Sarcastic Math Genius "),
            Text(mood, style: TextStyle(fontSize: 24)),
          ],
        ),
        backgroundColor: Colors.purple.shade300,
        elevation: 10,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.purple.shade100, Colors.pink.shade50],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            children: [
              Card(
                elevation: 8,
                color: Colors.white.withOpacity(0.9),
                child: Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      TextField(
                        controller: aController,
                        decoration: InputDecoration(
                          labelText: "First number (try not to break my brain)",
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.looks_one, color: Colors.purple),
                        ),
                        keyboardType: TextInputType.number,
                      ),
                      SizedBox(height: 16),
                      TextField(
                        controller: bController,
                        decoration: InputDecoration(
                          labelText: "Second number (I'm still processing the first one)",
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.looks_two, color: Colors.purple),
                        ),
                        keyboardType: TextInputType.number,
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 20),
              
              Card(
                elevation: 8,
                color: Colors.white.withOpacity(0.9),
                child: Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      Text("🎪 Choose Your Mathematical Adventure:", 
                           style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      SizedBox(height: 12),
                      Wrap(
                        spacing: 10,
                        runSpacing: 10,
                        children: [
                          ElevatedButton.icon(
                            onPressed: () => calculate("add"),
                            icon: Icon(Icons.add),
                            label: Text("Add"),
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                          ),
                          ElevatedButton.icon(
                            onPressed: () => calculate("multiply"),
                            icon: Icon(Icons.close),
                            label: Text("Multiply"),
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                          ),
                          ElevatedButton.icon(
                            onPressed: () => calculate("subtract"),
                            icon: Icon(Icons.remove),
                            label: Text("Subtract"),
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                          ),
                          ElevatedButton.icon(
                            onPressed: () => calculate("divide"),
                            icon: Icon(Icons.pie_chart),
                            label: Text("Divide"),
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              
              SizedBox(height: 20),
              
              Expanded(
                child: AnimatedBuilder(
                  animation: _shakeAnimation,
                  builder: (context, child) {
                    return Transform.translate(
                      offset: Offset(_shakeAnimation.value, 0),
                      child: Card(
                        elevation: 12,
                        color: Colors.yellow.shade50,
                        child: Container(
                          width: double.infinity,
                          padding: EdgeInsets.all(20),
                          child: SingleChildScrollView(
                            child: Text(
                              result,
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.w500,
                                color: Colors.purple.shade700,
                              ),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
              
              SizedBox(height: 10),
              Text(
                "💡 Pro tip: This calculator judges your math skills",
                style: TextStyle(
                  fontSize: 12,
                  fontStyle: FontStyle.italic,
                  color: Colors.grey.shade600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}