import sys, requests, json
sys.path.append('../..')
import go, tools

def vKw(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    vKwList = go.selectx('SELECT * FROM `botKeyword` WHERE `state`=1 and `uuid`="{0}"'.format(meta_data.get('uuid')))
    message = '[CQ:face,id=151] 小猪比机器人-关键词回复审核'
    for i in vKwList:
        message += '\n[CQ:face,id=161] 关键词：'+str(i.get('key'))+'\n      回复：'+str(i.get('value'))+'\n      ID：'+str(i.get('id'))
    go.send(meta_data, message)
    
def bKw(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    vKwList = go.selectx('SELECT * FROM `botKeyword` WHERE `state`=2 and `uuid`="{0}"'.format(meta_data.get('uuid')))
    message = '[CQ:face,id=151] 小猪比机器人-关键词回复垃圾箱'
    for i in vKwList:
        message += '\n[CQ:face,id=161] 关键词：'+str(i.get('key'))+'\n      回复：'+str(i.get('value'))+'\n      ID：'+str(i.get('id'))
    go.send(meta_data, message)
    
def tKw(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = message.split(' ')
    kwid = message1[0]
    iff = message1[1]
    if iff == '通过':
        state = 0
        message = '[CQ:face,id=161] 已通过！'
    else:
        state = 2
        message = '[CQ:face,id=161] 已移至回收站！'
    go.commonx('UPDATE `botKeyword` SET `state`='+str(state)+' WHERE `id`='+str(kwid)+' and `uuid`="{0}"'.format(meta_data.get('uuid')))
    tools.loadConfig(meta_data)
    go.send(meta_data, message)

def addKeyword(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    ob = tools.ReadCommandListener(meta_data)
    ob = json.loads(ob)
    if ob.get('code') == 404:
        tools.WriteCommandListener(meta_data, 'keyword.addKeyword(meta_data)', {'key':' ','value':' '})
        go.send(meta_data, '开始添加关键词回复，在此期间，你可以随时发送“退出”来退出加回复\n请发送触发该回复的关键词')
        go.send(meta_data, '提示：加回复规则详见：\nhttps://blog.xzy.center/archives/21/')
        return True
    
    step = int(ob.get('step'))
    args = ob.get('args')
    
    if step == 1:
        tools.WriteCommandListener(meta_data, args={'key':message,'value':' '})
        go.send(meta_data, '猪比知道了呢，那我该回答啥呢qwq？')
    
    if step == 2:
        tools.WriteCommandListener(meta_data, args={'key':args.get('key'),'value':message})
        go.send(meta_data, '好的呢，你希望用户的好感度至少为几的时候我会回答这条消息呢\n提示：未注册用户好感度-1，也就是说你如果想让该回复适用于所有用户请发送-1')
    
    if step == 3:
        key = args.get('key')
        value = args.get('value')
        tools.RemoveCommandListener(meta_data)
        
        if uid == meta_data.get('botSettings').get('owner'):
            sql = 'INSERT INTO `botKeyword` (`key`, `value`, `state`, `uid`, `coin`, `uuid`) VALUES ("'+str(key)+'", "'+str(value)+'", 0, '+str(uid)+', '+str(message)+', "'+str(meta_data.get('uuid'))+'");'
        else:
            sql = 'INSERT INTO `botKeyword` (`key`, `value`, `state`, `uid`, `coin`, `uuid`) VALUES ("'+str(key)+'", "'+str(value)+'", 1, '+str(uid)+', '+str(message)+', "'+str(meta_data.get('uuid'))+'");'
        go.commonx(sql)
        tools.loadConfig(meta_data)
        go.send(meta_data, '恭喜你，现在只需要等待我的主人审核通过后就可以啦！')
    
def delKeyword(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    sql = 'DELETE FROM `botKeyword` WHERE `key`="'+str(message)+'" and `uuid`="{0}"'.format(meta_data.get('uuid'))
    go.commonx(sql)
    tools.loadConfig(meta_data)
    go.send(meta_data, '[CQ:face,id=161] 删除成功！')
    
def listKeyword(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    message1 = '[CQ:face,id=151] 小猪比机器人-关键词回复列表'
    for i in go.keywordlist:
        message1 += '\n[CQ:face,id=161] 关键词：'+str(i.get('key'))+'\n      回复：'+str(i.get('value'))+'\n      ID：'+str(i.get('id'))
    go.send(meta_data ,message1)
    
def ListReplace(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    message = '[CQ:face,id=189] 小猪比机器人-关键词替换列表'
    for i in go.kwrlist:
        message += '\n[CQ:face,id=161] 字段：'+i.get('key')+'\n     解释：'+i.get('explain')
    go.send(meta_data, message)