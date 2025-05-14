# How to manage and access global state in Flutter? #

// 定义全局数据控制器
class GlobalController extends GetxController {
  final Rx<User?> currentUser = Rx<User?>(null);
  final RxBool isLoggedIn = false.obs;

  void setUser(User user) {
    currentUser.value = user;
    isLoggedIn.value = true;
  }

  void clearUser() {
    currentUser.value = null;
    isLoggedIn.value = false;
  }
}

// 在 main.dart 中初始化
void main() {
  Get.put(GlobalController());
  runApp(MyApp());
}

// 在任何地方访问
class SomeWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final controller = Get.find<GlobalController>();
    
    return Obx(() {
      if (controller.isLoggedIn.value) {
        return Text('Welcome ${controller.currentUser.value?.name}');
      }
      return LoginButton();
    });
  }
}