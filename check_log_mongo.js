// Скрипт проверяет состояние локальной базы данных getmyad (которая используется worker'ами)
// При необходимости восстанавливает
if (!db.log.impressions.validate().valid || !db.log.impressions.stats().capped) {
    print("Database log.impressions broken, recreating collections");
    db.log.impressions.drop();
    db.createCollection('log.impressions', {capped: true, max: 5000000, size: 5000000 * 500});
    db.log.impressions.ensureIndex({'token': 1});
}
else {
    print("Database log.impressions OK");
}
if (!db.log.impressions.block.validate().valid || !db.log.impressions.block.stats().capped) {
    print("Database log.impressions.block broken, recreating collections");
    db.log.impressions.block.drop();
    db.createCollection('log.impressions.block', {capped: true, max: 2000000, size: 2000000 * 200});
}
else {
    print("Database log.impressions.block OK");
}
if (!db.log.retargeting.validate().valid || !db.log.retargeting.stats().capped) {
    print("Database log.retargeting broken, recreating collections");
    db.log.retargeting.drop();
    db.createCollection('log.retargeting', {capped: true, max: 2000000, size: 2000000 * 200});
}
else {
    print("Database log.retargeting OK");
}