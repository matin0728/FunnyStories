```
    Create a Swift model and sub-model using following struct, and an initializer from type: "[String: AnyHashable]":
    
    {
        "activityId":1 , //1=签到活动
        "activityName":"签到活动" , //1=签到活动
        "activityRuleTile":"规则说明标题",
        "activityRuleContent":"规则说明的内容",
        "signInCount":2 , //签到次数
        "signInList":[
        {
            "signInDate":"2024-09-26 12:00:00"
            "isSignIn":true,
            "dueScore":5
        },
        {
            "signInDate":"2024-09-27 12:00:00"
            "isSignIn":false,
            "dueScore":10
        }
    }
```

```
Create a model for following data too:
    {
        "activityId":2 , //2=登录有礼
        "activityName":"登录有礼" , //2=登录有礼
        "activityRuleTile":"规则说明标题",
        "activityRuleContent":"规则说明的内容",
        "isFinish":true
    }
```