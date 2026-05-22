import '../../core/api_client.dart';

class RankingService {
  static Future<Map<String, dynamic>> getWeeklyRanking() async {
    return await ApiClient.get("/ranking/weekly");
  }
}
