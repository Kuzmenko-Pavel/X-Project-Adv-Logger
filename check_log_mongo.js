// Скрипт проверяет состояние локальной базы данных getmyad (которая используется worker'ами)
// При необходимости восстанавливает
var collection_name;
collection_name = 'log.click';
if (!db[collection_name].validate().valid || !db.log.click.stats().capped) {
    print("Database " + collection_name + " broken, recreating collections");
    db[collection_name].drop();
    db.createCollection(collection_name, {
        capped: true,
        max: 5000000,
        size: 5000000 * 1000
    });
    db[collection_name].ensureIndex({"dt": 1});
    db[collection_name].ensureIndex({
        "ip": 1,
        "dt": 1,
        "id_block": 1
    });
}
else {
    print("Database " + collection_name + " OK");
}

collection_name = 'blacklist';
if (!db[collection_name].validate().valid) {
    print("Database " + collection_name + " broken, recreating collections");
    db[collection_name].drop();
    db.createCollection(collection_name);
    db[collection_name].ensureIndex({"dt": 1});
    db[collection_name].ensureIndex({"ip": 1});
    db[collection_name].ensureIndex({
        'ip': 1,
        'cookie': 1
    });
}
else {
    print("Database " + collection_name + " OK");
}

collection_name = 'log.config';
if (!db[collection_name].validate().valid) {
    print("Database " + collection_name + " broken, recreating collections");
    db[collection_name].drop();
    db.createCollection(collection_name);
}
else {
    print("Database " + collection_name + " OK");
}

collection_name = 'log.impressions';
if (!db[collection_name].validate().valid || !db.log.click.stats().capped) {
    print("Database " + collection_name + " broken, recreating collections");
    db[collection_name].drop();
    db.createCollection(collection_name, {
        capped: true,
        max: 10000000,
        size: 10000000 * 1000
    });
    db[collection_name].ensureIndex({"token": 1});
}
else {
    print("Database " + collection_name + " OK");
}

collection_name = 'log.impressions.block';
if (!db[collection_name].validate().valid || !db.log.click.stats().capped) {
    print("Database " + collection_name + " broken, recreating collections");
    db[collection_name].drop();
    db.createCollection(collection_name, {
        capped: true,
        max: 5000000,
        size: 5000000 * 1000
    });
}
else {
    print("Database " + collection_name + " OK");
}


collection_name = 'log.goals';
if (!db[collection_name].validate().valid || !db.log.click.stats().capped) {
    print("Database " + collection_name + " broken, recreating collections");
    db[collection_name].drop();
    db.createCollection(collection_name, {
        capped: true,
        max: 5000000,
        size: 5000000 * 1000
    });
    db[collection_name].ensureIndex({"dt": 1});

}
else {
    print("Database " + collection_name + " OK");
}