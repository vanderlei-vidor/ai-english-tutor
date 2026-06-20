import 'package:flutter/material.dart';
import 'ranking_service.dart';

class RankingScreen extends StatefulWidget {
  const RankingScreen({super.key});

  @override
  State<RankingScreen> createState() => _RankingScreenState();
}

class _RankingScreenState extends State<RankingScreen>
    with TickerProviderStateMixin {
  List<dynamic> ranking = [];
  bool loading = true;
  
  late AnimationController _podiumController;
  late Animation<Offset> _podiumSlide;

  late AnimationController _glowController;
  late Animation<double> _glowAnimation;

  late AnimationController _crownController;
  late Animation<double> _crownFloat;

  final String currentUserId = "ad32edbf-b496-4e9a-9907-f52aba6a518d";

  @override
  void initState() {
    super.initState();

    _crownController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1600),
    );

    _crownFloat = Tween<double>(begin: -4, end: 4).animate(
      CurvedAnimation(parent: _crownController, curve: Curves.easeInOut),
    );

    _crownController.repeat(reverse: true);

    _glowController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);

    _glowAnimation = Tween<double>(begin: 4, end: 14).animate(
      CurvedAnimation(parent: _glowController, curve: Curves.easeInOut),
    );

    _podiumController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 900),
    );

    _podiumSlide = Tween<Offset>(begin: const Offset(0, 1.0), end: Offset.zero)
        .animate(
          CurvedAnimation(parent: _podiumController, curve: Curves.fastOutSlowIn),
        );

    loadRanking();
  }

  Future<void> loadRanking() async {
    try {
      final result = await RankingService.getWeeklyRanking();
      
      setState(() {
        if (result["ranking"] is List) {
          ranking = result["ranking"];
        } else {
          ranking = [];
        }
        loading = false;
        _podiumController.forward();
      });
    } catch (e) {
      setState(() => loading = false);
    }
  }

  Widget buildMedal(int position) {
    if (position == 1) return const Text("🥇", style: TextStyle(fontSize: 22));
    if (position == 2) return const Text("🥈", style: TextStyle(fontSize: 22));
    if (position == 3) return const Text("🥉", style: TextStyle(fontSize: 22));
    return Text(
      "$position",
      style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.grey),
    );
  }

  Widget buildUserTile(Map<String, dynamic> user) {
    bool isMe = user["user_id"] == currentUserId;
    
    String leagueIcon = "⭐";
    if (user["league"] is Map && user["league"]["icon"] != null) {
      leagueIcon = user["league"]["icon"];
    }

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 16),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: isMe
            ? Colors.greenAccent.withOpacity(0.1)
            : Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
        border: isMe ? Border.all(color: Colors.greenAccent, width: 1.5) : null,
      ),
      child: Row(
        children: [
          SizedBox(width: 35, child: buildMedal(user["position"] ?? 0)),
          const CircleAvatar(
            radius: 18,
            backgroundColor: Colors.blueAccent,
            child: Icon(Icons.person, color: Colors.white, size: 20),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              user["email"] ?? "Usuário",
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(
                color: isMe ? Colors.greenAccent : Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                "${user["weekly_xp"] ?? 0} XP",
                style: const TextStyle(
                  color: Colors.amber,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                leagueIcon,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _podiumController.dispose();
    _glowController.dispose();
    _crownController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0F172A), Color(0xFF020617)],
          ),
        ),
        child: SafeArea(
          child: loading
              ? const Center(child: CircularProgressIndicator(color: Colors.amber))
              : Column(
                  children: [
                    const SizedBox(height: 16),
                    const Text(
                      "🏆 Weekly Ranking",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    
                    // 🏆 PÓDIO BRINDADO CONTRA OVERFLOW
                    SlideTransition(
                      position: _podiumSlide,
                      child: buildPodium(ranking),
                    ),
                    const SizedBox(height: 12),
                    
                    // LISTA DO RESTANTE DOS USUÁRIOS
                    Expanded(
                      child: ListView.builder(
                        physics: const BouncingScrollPhysics(),
                        itemCount: ranking.length > 3 ? ranking.length - 3 : 0,
                        itemBuilder: (context, index) {
                          final userItem = Map<String, dynamic>.from(ranking[index + 3]);
                          return buildUserTile(userItem);
                        },
                      ),
                    ),
                  ],
                ),
        ),
      ),
    );
  }

  Widget buildPodium(List<dynamic> ranking) {
    if (ranking.isEmpty) return const SizedBox();

    // 🔥 ALTURA FIXA E SEGURA PARA O CONTAINER DO PÓDIO (Evita estouros)
    const double podiumHeight = 240.0;

    Map<String, dynamic>? first = ranking.isNotEmpty ? Map<String, dynamic>.from(ranking[0]) : null;
    Map<String, dynamic>? second = ranking.length > 1 ? Map<String, dynamic>.from(ranking[1]) : null;
    Map<String, dynamic>? third = ranking.length > 2 ? Map<String, dynamic>.from(ranking[2]) : null;

    return Container(
      height: podiumHeight,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // 2º Lugar (Esquerda) - Bloco de 65px de altura
          if (second != null)
            Expanded(
              child: buildPodiumItem(second, 2, 65.0, Colors.grey.shade400),
            )
          else
            const Expanded(child: SizedBox()),

          // 1º Lugar (Centro) - Bloco de 90px de altura
          if (first != null)
            Expanded(
              child: buildPodiumItem(first, 1, 90.0, Colors.amber),
            )
          else
            const Expanded(child: SizedBox()),

          // 3º Lugar (Direita) - Bloco de 45px de altura
          if (third != null)
            Expanded(
              child: buildPodiumItem(third, 3, 45.0, Colors.brown.shade400),
            )
          else
            const Expanded(child: SizedBox()),
        ],
      ),
    );
  }

  Widget buildPodiumItem(
    Map<String, dynamic> user,
    int position,
    double blockHeight,
    Color color,
  ) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.end,
      mainAxisSize: MainAxisSize.min, // Garante compactação vertical precisa
      children: [
        SizedBox(
          height: 75,
          child: Stack(
            clipBehavior: Clip.none,
            alignment: Alignment.center,
            children: [
              if (position == 1)
                Positioned(
                  top: -16,
                  child: AnimatedBuilder(
                    animation: _crownFloat,
                    builder: (context, child) {
                      return Transform.translate(
                        offset: Offset(0, _crownFloat.value),
                        child: const Text("👑", style: TextStyle(fontSize: 28)),
                      );
                    },
                  ),
                ),
              Positioned(
                bottom: 4,
                child: CircleAvatar(
                  radius: position == 1 ? 28 : 22,
                  backgroundColor: color.withOpacity(0.2),
                  child: CircleAvatar(
                    radius: position == 1 ? 24 : 19,
                    backgroundColor: Colors.grey.shade800,
                    child: const Icon(Icons.person, color: Colors.white, size: 20),
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 4),
        Text(
          user["email"]?.split('@')[0] ?? "Player",
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.white,
            fontSize: 12,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          "⭐ ${user["weekly_xp"] ?? 0}",
          style: const TextStyle(color: Colors.amber, fontSize: 11, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        
        // 🛠️ REMOVIDO o Expanded externo que conflitava com a altura do container interno
        AnimatedBuilder(
          animation: _glowAnimation,
          builder: (context, child) {
            return Container(
              height: blockHeight,
              width: 65,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [color, color.withOpacity(0.4)],
                ),
                borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
                boxShadow: [
                  if (position == 1)
                    BoxShadow(
                      color: Colors.amber.withOpacity(0.4),
                      blurRadius: _glowAnimation.value,
                      spreadRadius: 1,
                    ),
                ],
              ),
              child: Center(
                child: Text(
                  "$positionº",
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 15,
                  ),
                ),
              ),
            );
          },
        ),
      ],
    );
  }
}