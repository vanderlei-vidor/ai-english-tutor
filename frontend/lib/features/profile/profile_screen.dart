import 'package:flutter/material.dart';
import '../../models/profile_model.dart';
import 'profile_service.dart';

class ProfileScreen extends StatefulWidget {
  final String userId;

  const ProfileScreen({Key? key, required this.userId}) : super(key: key);

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  late Future<ProfileModel> profileFuture;

  @override
  void initState() {
    super.initState();
    profileFuture = ProfileService().fetchProfile(widget.userId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F111A),
      body: SafeArea(
        child: FutureBuilder<ProfileModel>(
          future: profileFuture,
          builder: (context, snapshot) {
            if (!snapshot.hasData) {
              return const Center(
                child: CircularProgressIndicator(color: Colors.amber),
              );
            }

            final profile = snapshot.data!;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [

                  /// 🔥 HEADER
                  Row(
                    children: [
                      const CircleAvatar(
                        radius: 30,
                        backgroundColor: Colors.amber,
                        child: Icon(Icons.person, size: 30, color: Colors.black),
                      ),
                      const SizedBox(width: 16),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "League: ${profile.userLeague}",
                            style: const TextStyle(
                              color: Colors.amber,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            "CEFR ${profile.levelCode} • ${profile.levelLabel}",
                            style: const TextStyle(color: Colors.white70),
                          ),
                        ],
                      )
                    ],
                  ),

                  const SizedBox(height: 30),

                  /// 🚀 XP CARD
                  _buildXpCard(profile),

                  const SizedBox(height: 20),

                  /// 🔥 STREAK CARD
                  _buildStreakCard(profile),

                  const SizedBox(height: 20),

                  /// 📊 STATS CARD
                  _buildStatsCard(profile),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildXpCard(ProfileModel profile) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF1C1F2A),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "XP Progress",
            style: TextStyle(color: Colors.white, fontSize: 18),
          ),
          const SizedBox(height: 12),
          LinearProgressIndicator(
            value: profile.xpProgress / 100,
            backgroundColor: Colors.grey[800],
            valueColor: const AlwaysStoppedAnimation(Colors.amber),
            minHeight: 8,
          ),
          const SizedBox(height: 12),
          Text(
            "Level ${profile.xpLevel} • ${profile.totalXp} XP",
            style: const TextStyle(color: Colors.white70),
          )
        ],
      ),
    );
  }

  Widget _buildStreakCard(ProfileModel profile) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF1C1F2A),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            "🔥 Streak",
            style: TextStyle(color: Colors.white, fontSize: 18),
          ),
          Column(
            children: [
              Text(
                "${profile.streakCurrent} days",
                style: const TextStyle(
                    color: Colors.orange,
                    fontSize: 20,
                    fontWeight: FontWeight.bold),
              ),
              Text(
                "Best: ${profile.streakLongest}",
                style: const TextStyle(color: Colors.white54),
              ),
            ],
          )
        ],
      ),
    );
  }

  Widget _buildStatsCard(ProfileModel profile) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF1C1F2A),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Statistics",
            style: TextStyle(color: Colors.white, fontSize: 18),
          ),
          const SizedBox(height: 15),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _statItem("Conversations", profile.totalConversations.toString()),
              _statItem("Score", "${profile.globalScore}%"),
            ],
          )
        ],
      ),
    );
  }

  Widget _statItem(String title, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: const TextStyle(color: Colors.white54)),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
}
