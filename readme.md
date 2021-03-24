# 内存数据库
## 订单表
订单号(TicketNum)  
送的地址(Taddress)  
外卖的位置(Gaddress)  
外卖物品(Item)  
预计到达时间(Time)  
手机尾号(phoneNum)  
下单人学号(StudentNum)  
接单人学号(BroNum)  
收到确认码(CertiCode)  
下单时间(BeginTime)  
订单状态(Status)
# 硬盘数据库
## 用户表
学号(StudentNum)  
密码(password)  
邮箱(email)  
## 历史表
订单号(TicketNum)  
外卖物品(Item)  
下单时间(BeginTime)  
下单人学号(StudentNum)  
接单人学号(BroNum)  
送的地址(Taddress)

# 数据包

(采用UDP发送符合json标准的字符串完成，为便于调试，暂定最长1k个字符)
## 注册用户(register)
>{
    "type":"register",
    "StudentNum":"",
    "password":"",
    "email":""
}
## 返回
>{
    "respond":"true"
}

或
>{
    "respond":"false"
}
## 登录
>{
    "type":"login",
    "StudentNum":"",
    "password":""
}
## 返回
>{
    "respond":"true"
}

或
>{
    "respond":"false"
}
## 修改密码
>{
    "type":"changePassword",
    "StudentNum":"",
    "oldPassword":"",
    "newPassword":""
}
## 返回
>{
    "respond":"true"
}

或
>{
    "respond":"false"
}
## 请求邮箱
>{
    "type":"getEmail",
    "StudentNum":""
}
## 返回
>{
    "email":""
}
## 发单
>{
    "type":"postOrder",
    "Taddress":"",
    "Gaddress":"",
    "Item":"",
    "Time":"",
    "phoneNum":"",
    "StudentNum":""
}
## 返回
>{
    "TicketNum":"",
    "CertiCode":""
}
## 接单
>{
    "type":"getOrder",
    "Num":"",
    "Gaddress":""
}
## 返回
>[  
    {
        "TicketNum":"",
        "Taddress":"",
        "Gaddress":"",
        "Item":"",
        "Time":"",
        "phoneNum":"",
        "BeginTime":""
    }  
    ......  
]
## 确认订单
>{
    "type":"INeedMoney",
    "TicketNum":"",
    "StudentNum":""
}
## 返回
>{
    "TicketNum":"",
    "respond":"true"
}

或
>{
    "TicketNum":"",
    "respond":"false"
}
## 请求下单状态
>{
    "type":"getOrderStatus",
    "StudentNum":""
}
## 返回
>[  
    {
        "TicketNum":"",
        "Status":""
    }  
    ......  
]
## 请求接单状态
>{
    "type":"getWorkingStatus",
    "StudentNum":""
}
## 返回
>[  
    {
        "TicketNum":"",
        "Status":""
    }  
    ......  
]
## 请求订单状态
>{
    "type":"getTicketStatus",
    "TicketNum":""
}
## 返回
>{
        "TicketNum":"",
        "Status":""
}
## 请求订单全信息
>{
    "type":"getTicketAllInfo",
    "TicketNum":""
}
## 返回
>{
    "TicketNum":"",
    "Taddress":"",
    "Gaddress":"",
    "Item":"",
    "Status":"",
    "StudentNum":"",
    "BroNum":"",
    "phoneNum":"",
    "CertiCode":""
}
## 取消订单
>{
    "type":"cancelTicket",
    "TicketNum":""
}
## 返回
>{
    "respond":"true"
}

或
>{
    "respond":"false"
}
## 忘记密码
>{
    "type":"forgetPassword",
    "StudentNum":""
}
## 返回
>{
    "respond":"true"
}

或
>{
    "respond":"false"
}
## 请求所有在线订单
>{
    "type":"AdminRequire"
}
## 返回
>[  
    {
        "TicketNum":"",
        "Taddress":"",
        "Gaddress":"",
        "Item":"",
        "Status":"",
        "StudentNum":"",
        "BroNum":""
    }  
    ......  
]
## 铁拳干碎订单
>{
    "type":"Terminate",
    "TicketNum":""
}
## 返回
无需返回
## 查询历史订单
>{
    "type":"getHistory",
    "StudentNum":""
}
## 返回
>[
    {
    "TicketNum":"",
    "Item":"",
    "BeginTime":"",
    "StudentNum":"",
    "BroNum":"",
    "Taddress":""
    }
    ......
]
## 确认订单已经完成
>{
    "type":"confirmTicketDone"
    "TicketNum":""
}
## 返回
>{
    "TicketNum":"",
    "respond":"true"
}

或
>{
    "TicketNum":"",
    "respond":"false"
}