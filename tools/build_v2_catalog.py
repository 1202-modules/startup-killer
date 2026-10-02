"""Apply the four owner-approved v2 card tables to the static catalog."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/attack_choices.json'
data = json.loads(path.read_text())
# Each entry: title, action, consequence, base stream losses, duration, incident RUB,
# reputation delta, initial flag, combo stream losses, combo incident RUB,
# combo reputation delta, combo prerequisite, combo flag.
TABLE = {
'petmind': [
('РАЗОБЛАЧИТЬ ЗАЯВЛЕННЫЕ «96%»','Провести независимый тест PetMind и публично показать ошибки распознавания.','Покупатели сомневаются в точности ошейника и реже оформляют подписку.',{'collars':600,'subscription':800},'temporary',0,-3,'accuracy_doubted'),
('ПЕРЕХВАТИТЬ ПРОИЗВОДСТВЕННЫЕ МОЩНОСТИ','Законтрактовать свободные мощности единственного завода перед следующей партией PetMind.','Следующая партия ошейников задерживается, а компания несёт расходы на перестройку поставки.',{'collars':1000},'temporary',120000,0,'factory_pressure'),
('ОБЕСЦЕНИТЬ ПЛАТНУЮ ПОДПИСКУ','Выпустить бесплатный сервис с функциями платной подписки PetMind.','Часть пользователей перестаёт платить за подписку.',{'subscription':1200},'temporary',0,0,'free_alternative'),
('ВЫДАВИТЬ PETMIND ДЕШЁВЫМ ОШЕЙНИКОМ','Вывести простой трекер значительно дешевле PetMind.','Продажи ошейников падают из-за дешёвого конкурента.',{'collars':1700},'temporary'),
('РАЗОГНАТЬ ДОКАЗАННЫЕ ОШИБКИ','Распространить результаты теста через профильные сообщества и обзоры.','Недоверие снижает продажи ошейников и подписки.',{'collars':1200,'subscription':1500},'persistent',0,0,None,{'collars':2600,'subscription':3200},0,-8,'accuracy_doubted','trust_crisis'),
('СОРВАТЬ СЛЕДУЮЩУЮ ПАРТИЮ','Перекупить производственные слоты, необходимые для новой партии PetMind.','Дефицит ошейников срывает продажи и вызывает дополнительные расходы.',{'collars':1800},'persistent',100000,0,None,{'collars':4200},250000,0,'factory_pressure','stockout'),
('ПЕРЕМАНИТЬ ПОДПИСЧИКОВ','Предложить пользователям PetMind перенос истории и бесплатный переход.','Платные подписчики уходят к конкуренту.',{'subscription':2000},'persistent',0,0,None,{'subscription':4200},0,0,'free_alternative','churn_wave'),
('ЗАДУШИТЬ ПРОДАЖИ ЦЕНОВОЙ ВОЙНОЙ','Снизить цену конкурирующего ошейника и расширить продажи.','PetMind теряет покупателей ошейников.',{'collars':2800},'persistent'),
('СОРВАТЬ ВЕТЕРИНАРНЫЕ РЕКОМЕНДАЦИИ','Передать ветеринарным сетям доказательства ошибок PetMind и предложить альтернативу.','Потеря рекомендаций снижает продажи и подписку.',{'collars':1600,'subscription':2000},'structural',0,0,None,{'collars':4300,'subscription':5400},0,-12,'trust_crisis'),
('ЗАБРАТЬ ПОКУПАТЕЛЕЙ ВО ВРЕМЯ ДЕФИЦИТА','Предложить ожидающим ошейники PetMind немедленную поставку своего устройства.','Покупатели переходят к конкуренту; восстановление завода не возвращает их автоматически.',{'collars':2000},'structural',0,0,None,{'collars':6800},120000,0,'stockout'),
('ДОБИТЬ ПОДПИСКУ БЕСПЛАТНЫМ АНАЛОГОМ','Перевести пользователей на бесплатный аналог с сохранением их данных.','Массовый уход подписчиков снижает и спрос на ошейники.',{'subscription':2400},'structural',0,0,None,{'subscription':9000,'collars':5500},0,0,'churn_wave'),
('ПЕРЕХВАТИТЬ РЫНОК КОМПЛЕКТОМ БЕЗ АБОНПЛАТЫ','Продать конкурентный трекер с сервисом без ежемесячной платы.','PetMind теряет продажи ошейников и подписки.',{'collars':2600,'subscription':2400},'structural'),
],
'coffeebot': [
('ПЕРЕХВАТИТЬ КАМПУСНЫЙ ТРАФИК','Открыть конкурирующие кофейные точки на основных маршрутах студентов.','Поток покупателей у киосков CoffeeBot уменьшается.',{'kiosks':1000},'temporary',0,0,'footfall_contested'),
('УДАРИТЬ ПО РЕПУТАЦИИ ПРОСТОЯМИ','Публично собрать и распространить подтверждённые случаи простоя CoffeeBot.','Клиенты реже покупают кофе и заключают сервисные договоры.',{'kiosks':500,'service':800},'temporary',0,-2,'uptime_exposed'),
('НАЧАТЬ ЦЕНОВУЮ ВОЙНУ','Поставить рядом автоматы с более дешёвым кофе.','Часть продаж CoffeeBot уходит к дешёвому конкуренту.',{'kiosks':1200},'temporary',0,0,'price_pressure'),
('ПЕРЕМАНИТЬ ОФИСНЫХ КЛИЕНТОВ','Предложить офисам обслуживание кофеен на лучших условиях.','CoffeeBot теряет сервисные контракты.',{'service':1800},'temporary'),
('ЗАБРАТЬ ЛУЧШИЕ ТОЧКИ В КАМПУСАХ','Заключить договоры на наиболее проходные места в кампусах.','Киоски CoffeeBot теряют важные точки продаж.',{'kiosks':1500},'persistent',0,0,None,{'kiosks':3400},0,0,'footfall_contested','campus_locked'),
('СОРВАТЬ РЕМОНТ И ОБСЛУЖИВАНИЕ','Переманить ключевых ремонтных подрядчиков CoffeeBot.','Простои снижают продажи и сервисную выручку.',{'kiosks':1200,'service':1800},'persistent',200000,0,None,{'kiosks':3200,'service':4200},350000,0,'uptime_exposed','repair_backlog'),
('УСИЛИТЬ ЦЕНОВУЮ ВОЙНУ','Расширить сеть дешёвых автоматов рядом с CoffeeBot.','Продажи киосков CoffeeBot падают.',{'kiosks':2000},'persistent',0,0,None,{'kiosks':3800},0,0,'price_pressure','margin_squeeze'),
('ПЕРЕМАНИТЬ ОФИСЫ БЕСПЛАТНЫМ ПЕРЕХОДОМ','Оплатить офисам переход на свой сервис.','CoffeeBot теряет корпоративную сервисную выручку.',{'service':3000},'persistent'),
('ВЫТЕСНИТЬ COFFEEBOT ИЗ КЛЮЧЕВЫХ КАМПУСОВ','Занять оставшиеся ключевые места конкурирующими кофейными точками.','Продажи CoffeeBot в кампусах надолго падают.',{'kiosks':2200},'structural',0,0,None,{'kiosks':8600},0,0,'campus_locked'),
('ЗАБРАТЬ КЛИЕНТОВ НА ФОНЕ ПРОСТОЕВ','Предложить клиентам CoffeeBot немедленную замену простаивающих точек.','Клиенты уходят; ремонт автоматов не возвращает их автоматически.',{'kiosks':2200,'service':3500},'structural',100000,0,None,{'kiosks':6200,'service':9000},900000,0,'repair_backlog'),
('ДОБИТЬ ОСНОВНЫЕ ПРОДАЖИ ДЕМПИНГОМ','Предложить кофе дешевле CoffeeBot в большинстве его точек.','Основные продажи киосков переходят конкуренту.',{'kiosks':2800},'structural',0,0,None,{'kiosks':8800},0,0,'margin_squeeze'),
('ЗАБРАТЬ КОРПОРАТИВНЫЕ КОНТРАКТЫ','Заключить долгосрочные договоры с офисными клиентами CoffeeBot.','Сервисная выручка CoffeeBot надолго снижается.',{'service':5500},'structural'),
],
'foodrover': [
('ЗАПУСТИТЬ ПРОВЕРКУ МАРШРУТОВ','Подать обоснованное обращение о безопасности маршрутов FoodRover.','Проверка замедляет доставку и ухудшает доверие.',{'delivery':800},'temporary',0,-2,'route_scrutiny'),
('СКУПИТЬ ДОСТУПНЫЕ БАТАРЕИ','Выкупить доступные сменные аккумуляторы перед закупкой FoodRover.','Роботы простаивают, обслуживание дорожает.',{'delivery':800,'maintenance':500},'temporary',150000,0,'battery_pressure'),
('ПЕРЕМАНИТЬ РЕСТОРАНЫ ДЕШЁВЫМИ КУРЬЕРАМИ','Предложить ресторанам более дешёвую альтернативную доставку.','Часть заказов уходит от FoodRover.',{'delivery':1200},'temporary',0,0,'competitor_trial'),
('ПЕРЕМАНИТЬ СЕРВИСНЫХ КЛИЕНТОВ','Предложить владельцам роботов конкурирующий сервис.','FoodRover теряет сервисную выручку.',{'maintenance':1500},'temporary'),
('ДОБИТЬСЯ ОГРАНИЧЕНИЙ НА КЛЮЧЕВЫХ МАРШРУТАХ','Предоставить регулятору данные проверки и добиться ограничений маршрутов.','Доставка замедляется и требует расходов на обходные пути.',{'delivery':1800},'persistent',0,0,None,{'delivery':3800},100000,-3,'route_scrutiny','route_restricted'),
('ПЕРЕХВАТИТЬ ПОСТАВКУ АККУМУЛЯТОРОВ','Законтрактовать остаток аккумуляторов у поставщика FoodRover.','Доставка и обслуживание страдают от дефицита.',{'delivery':1800,'maintenance':1500},'persistent',150000,0,None,{'delivery':4200,'maintenance':3200},350000,0,'battery_pressure','battery_backlog'),
('УВЕСТИ РЕСТОРАНЫ С FOODROVER','Предложить ресторанам полный переход на конкурирующую доставку.','FoodRover теряет ресторанные заказы.',{'delivery':2000},'persistent',0,0,None,{'delivery':4200},0,0,'competitor_trial','restaurant_switch'),
('ЗАБРАТЬ СЕРВИС ГАРАНТИЕЙ 24 ЧАСА','Предложить сервисным клиентам гарантию ремонта за сутки.','Сервисные контракты уходят к конкуренту.',{'maintenance':2500},'persistent'),
('ЗАКРЫТЬ FOODROVER ДОСТУП К КЛЮЧЕВОМУ РАЙОНУ','Добиться ограничения доступа роботов в самый важный район.','Район становится недоступным для доставок FoodRover.',{'delivery':2400},'structural',0,0,None,{'delivery':7400},250000,-4,'route_restricted'),
('ЗАБРАТЬ РЕСТОРАНЫ НА ФОНЕ ПРОСТОЕВ','Предложить ресторанам надёжную доставку, пока роботы FoodRover простаивают.','Рестораны уходят; новые аккумуляторы не возвращают их автоматически.',{'delivery':2600,'maintenance':2000},'structural',100000,0,None,{'delivery':7200,'maintenance':5500},500000,0,'battery_backlog'),
('ЗАБЛОКИРОВАТЬ ВОЗВРАТ РЕСТОРАНОВ','Подписать с перешедшими ресторанами долгосрочные эксклюзивные договоры.','FoodRover не может вернуть ресторанные заказы.',{'delivery':3000},'structural',0,0,None,{'delivery':8000},0,0,'restaurant_switch'),
('ПЕРЕХВАТИТЬ СЕРВИСНЫЕ КОНТРАКТЫ','Заключить эксклюзивные договоры с сервисными клиентами FoodRover.','Сервисная выручка надолго уходит к конкуренту.',{'maintenance':4000},'structural'),
],
'studygenie': [
('НАЙТИ И ОПУБЛИКОВАТЬ ОШИБКИ','Проверить ответы StudyGenie и публично показать подтверждённые ошибки.','Подписчики и школы теряют доверие.',{'subscriptions':900,'schools':700},'temporary',0,-3,'quality_doubt'),
('ЗАБРАТЬ РЕЗЕРВ API-МОЩНОСТИ','Законтрактовать доступную приоритетную квоту внешнего AI-провайдера.','В экзаменационный сезон StudyGenie испытывает перебои и расходы.',{'subscriptions':800,'schools':500},'temporary',100000,0,'api_pressure'),
('ОТТЯНУТЬ УЧЕНИКОВ БЕСПЛАТНОЙ ПОДГОТОВКОЙ','Запустить бесплатную подготовку с переносом прогресса учеников.','Часть учеников отменяет подписку StudyGenie.',{'subscriptions':1200},'temporary',0,0,'exam_trial'),
('ЗАЙТИ В ШКОЛЫ БЕСПЛАТНЫМ ПИЛОТОМ','Предложить школам бесплатный пилот конкурирующего сервиса.','StudyGenie теряет школьные продажи.',{'schools':1200},'temporary'),
('ДОКАЗАТЬ, ЧТО ОШИБКИ СИСТЕМНЫЕ','Расширить тестирование и опубликовать повторяющиеся ошибки StudyGenie.','Подписчики и школы сокращают закупки.',{'subscriptions':1200,'schools':1000},'persistent',0,0,None,{'subscriptions':3000,'schools':2800},0,-7,'quality_doubt','trust_crisis'),
('ОСТАВИТЬ STUDYGENIE БЕЗ API-РЕЗЕРВА','Перехватить доступную резервную квоту перед экзаменами.','Перебои снижают подписки и школьные продажи.',{'subscriptions':1200,'schools':800},'persistent',100000,0,None,{'subscriptions':3800,'schools':3000},300000,0,'api_pressure','api_bottleneck'),
('ПЕРЕМАНИТЬ УЧЕНИКОВ БЕЗ ПОТЕРИ ПРОГРЕССА','Предложить ученикам перенос их истории в конкурирующий сервис.','StudyGenie теряет подписчиков.',{'subscriptions':1600},'persistent',0,0,None,{'subscriptions':4000},0,0,'exam_trial','cohort_churn'),
('ПЕРЕМАНИТЬ МЕТОДСОВЕТЫ','Предложить методическим советам конкурирующий школьный продукт.','StudyGenie теряет школьные лицензии.',{'schools':2200},'persistent'),
('СОРВАТЬ ПРОДЛЕНИЕ ШКОЛЬНЫХ ЛИЦЕНЗИЙ','Передать школам доказательства ошибок и предложить замену StudyGenie.','Школы отказываются от продления, подписки тоже снижаются.',{'subscriptions':1400,'schools':2200},'structural',0,0,None,{'subscriptions':4800,'schools':7200},0,-10,'trust_crisis'),
('УВЕСТИ ПОЛЬЗОВАТЕЛЕЙ ВО ВРЕМЯ СБОЕВ','Предложить пользователям StudyGenie стабильную альтернативу во время перебоев.','Пользователи уходят; восстановление квоты не возвращает их автоматически.',{'subscriptions':1800,'schools':1500},'structural',0,0,None,{'subscriptions':7200,'schools':5500},150000,-4,'api_bottleneck'),
('ДОБИТЬ УЧЕНИЧЕСКУЮ ПОДПИСКУ БЕСПЛАТНЫМ АНАЛОГОМ','Перевести учеников на бесплатную альтернативу с сохранением прогресса.','Платные ученические подписки массово прекращаются.',{'subscriptions':2400},'structural',0,0,None,{'subscriptions':8800},0,0,'cohort_churn'),
('ЗАБРАТЬ ГОДОВЫЕ ЛИЦЕНЗИИ ШКОЛ','Заключить годовые договоры со школами вместо StudyGenie.','Школьные лицензии уходят конкуренту.',{'schools':4000},'structural'),
],
}
for item in data['choices']:
    slug = item['startup_slug']
    if slug not in TABLE:
        continue
    r = item['round_number']
    suffix = item['id'].rsplit('_', 1)[1]
    old_index = int(suffix) - 1 if suffix.isdigit() else 'abcd'.index(suffix)
    letter = 'ABCD'[old_index]
    row = TABLE[slug][(r - 1) * 4 + old_index]
    title, action, result, streams, duration, *rest = row
    incident = rest[0] if len(rest) > 0 else 0
    reputation = rest[1] if len(rest) > 1 else 0
    initial_flag = rest[2] if len(rest) > 2 else None
    combo_streams = rest[3] if len(rest) > 3 else None
    combo_incident = rest[4] if len(rest) > 4 else 0
    combo_reputation = rest[5] if len(rest) > 5 else 0
    prerequisite = rest[6] if len(rest) > 6 else None
    combo_flag = rest[7] if len(rest) > 7 else None
    group = f'{slug}_{letter.lower()}'
    item['title'] = title
    item['short_description'] = action
    item['result_headline'] = title
    item['duration'] = duration
    item['stack_group'] = group
    kind = {
        'petmind': ('reputation', 'supply', 'competition', 'competition'),
        'coffeebot': ('competition', 'technology', 'competition', 'competition'),
        'foodrover': ('supply', 'supply', 'competition', 'competition'),
        'studygenie': ('reputation', 'technology', 'competition', 'competition'),
    }[slug][old_index]
    if r == 3 and letter == 'B':
        kind = 'competition'
    item['attack_type'] = kind
    item['scene_type'] = kind
    item['weakness_id'] = None
    item['weakness_match'] = 'normal'
    item['evidence_fact_ids'] = [item['evidence_fact_ids'][0]]
    item['target_stream_ids'] = list(streams)
    item['narrative'] = {'attack': action, 'company_response': 'Команда оценивает ущерб и выбирает защиту по прогнозу.', 'result': result}
    base = {'stream_loss_bps': streams, 'duration': duration, 'incident_cost_kopeks': incident * 100, 'reputation_delta': reputation, 'set_flags': [initial_flag] if initial_flag else []}
    effect = {'group': group, 'base_effect': base}
    if combo_streams:
        effect['combo'] = {'requires_all': [prerequisite], 'stream_loss_bps': combo_streams, 'duration': duration, 'incident_cost_kopeks': combo_incident * 100, 'reputation_delta': combo_reputation, 'set_flags': [combo_flag] if combo_flag else []}
    if r == 3 and letter == 'B':
        effect['cause'] = 'customer_churn'
    item['v2_effect'] = effect
    item['id'] = f'{slug}_r{r}_{letter.lower()}'
data['catalog_version'] = '2.0.0-partial'
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
