import '../../core/api_client.dart';
import '../../models/profile_model.dart';

class ProfileService {
  Future<ProfileModel> fetchProfile(String userId) async {
    final response = await ApiClient.get('/profile/$userId');

    return ProfileModel.fromJson(response);
  }
}
