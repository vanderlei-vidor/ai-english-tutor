class ProfileModel {
  final String userId;
  final String userLeague;
  final int totalConversations;
  final int globalScore;
  final String levelCode;
  final String levelLabel;
  final int streakCurrent;
  final int streakLongest;
  final int totalXp;
  final int xpLevel;
  final int xpProgress;

  ProfileModel({
    required this.userId,
    required this.userLeague,
    required this.totalConversations,
    required this.globalScore,
    required this.levelCode,
    required this.levelLabel,
    required this.streakCurrent,
    required this.streakLongest,
    required this.totalXp,
    required this.xpLevel,
    required this.xpProgress,
  });

  factory ProfileModel.fromJson(Map<String, dynamic> json) {
    return ProfileModel(
      userId: json['user_id'],
      userLeague: json['user_league'],
      totalConversations: json['stats']['total_conversations'],
      globalScore: json['stats']['global_score'],
      levelCode: json['level']['code'],
      levelLabel: json['level']['label'],
      streakCurrent: json['streak']['current'],
      streakLongest: json['streak']['longest'],
      totalXp: json['xp']['total_xp'],
      xpLevel: json['xp']['level_data']['level'],
      xpProgress: json['xp']['level_data']['progress_percentage'],
    );
  }
}
