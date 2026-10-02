"""Install the owner-approved v2 catalog for the six remaining startups."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/attack_choices.json"

def card(title, action, result, base, duration, incident=0, rep=0, flag=None,
         combo=None, combo_incident=0, combo_rep=0, requires=None, combo_flag=None,
         cause=None):
    effect = {"group": "", "base_effect": {
        "stream_loss_bps": base, "duration": duration,
        "incident_cost_kopeks": incident * 100, "reputation_delta": rep,
        "set_flags": [flag] if flag else [],
    }}
    if combo:
        effect["combo"] = {"requires_all": [requires], "stream_loss_bps": combo,
                            "duration": duration, "incident_cost_kopeks": combo_incident * 100,
                            "reputation_delta": combo_rep,
                            "set_flags": [combo_flag] if combo_flag else []}
    if cause:
        effect["cause"] = cause
    return {"title": title, "action": action, "result": result, "effect": effect}

CARDS = {
"sleepwork": [
card("ДОКАЗАТЬ HR, ЧТО КАПСУЛЫ ПРОСТАИВАЮТ", "Провести аудит загрузки и показать клиентам SleepWork, что при гибридной работе капсулы большую часть времени пустуют.", "HR сомневаются в загрузке и сокращают аренду капсул.", {"leases":800}, "temporary", flag="utilization_exposed"),
card("ПОКАЗАТЬ ЦЕНУ КАЖДОГО МЕТРА ПОД КАПСУЛОЙ", "Посчитать стоимость занимаемой площади и показать HR, сколько офис платит за малоиспользуемую зону.", "Клиенты видят низкую отдачу площади и пересматривают аренду.", {"leases":700}, "temporary", flag="space_cost_exposed"),
card("ЗАПУСТИТЬ WELLNESS БЕЗ КАПСУЛ", "Предложить компаниям более дешёвую программу отдыха и восстановления без аренды оборудования.", "Компании сокращают аренду оборудования в пользу программы без капсул.", {"wellness":1800,"leases":400}, "temporary", flag="no_hardware_trial"),
card("СДАТЬ КАПСУЛЫ ДЕШЕВЛЕ", "Вывести прямой аналог с меньшей ежемесячной арендой.", "SleepWork теряет клиентов из-за более дешёвой аренды.", {"leases":1000}, "temporary"),
card("СОРВАТЬ ПРОДЛЕНИЯ АРЕНДЫ", "Использовать данные низкой загрузки перед продлением договоров и убедить HR отказаться от части капсул.", "Продления сокращаются, а wellness-бюджеты тоже пересматриваются.", {"leases":1600}, "persistent", combo={"leases":3600,"wellness":1200}, requires="utilization_exposed", combo_flag="renewal_risk"),
card("ПЕРЕМАНИТЬ ПЛОЩАДЬ ПОД БОЛЕЕ ВЫГОДНЫЕ ОФИСНЫЕ ЗОНЫ", "Предложить компаниям заменить зоны с капсулами переговорными и рабочими местами с более понятной отдачей.", "Площади под капсулы перераспределяются; SleepWork несёт расходы.", {"leases":1800}, "persistent", incident=100000, combo={"leases":4000}, combo_incident=250000, requires="space_cost_exposed", combo_flag="space_reallocation"),
card("ПЕРЕМАНИТЬ HR НА WELLNESS БЕЗ ОБОРУДОВАНИЯ", "Дать компаниям миграцию на более дешёвую wellness-программу и убрать необходимость арендовать капсулы.", "Клиенты уходят в wellness без оборудования.", {"wellness":3000,"leases":1000}, "persistent", combo={"wellness":5500,"leases":2800}, requires="no_hardware_trial", combo_flag="wellness_switch"),
card("ПЕРЕМАНИТЬ КРУПНЫХ АРЕНДАТОРОВ", "Дать крупным офисам скидку за переход на капсулы конкурента.", "Крупные арендаторы сокращают договоры SleepWork.", {"leases":1800}, "persistent"),
card("ПЕРЕНАПРАВИТЬ WELLNESS-БЮДЖЕТ ИЗ КАПСУЛ В ЛЬГОТЫ ДЛЯ УДАЛЁНЩИКОВ", "Предложить HR направить wellness-бюджет на домашний спорт, терапию и другие льготы вместо аренды SleepWork.", "Корпоративный бюджет уходит из капсул в льготы для удалёнщиков.", {"leases":1600,"wellness":1000}, "persistent", combo={"leases":7800,"wellness":4500}, requires="renewal_risk"),
card("ВЫТЕСНИТЬ КАПСУЛЫ ИЗ КЛЮЧЕВЫХ ОФИСОВ", "Закрепить перепланировку офисов и добиться расторжения договоров SleepWork на основных площадках.", "Ключевые договоры отменяются; это потерянные контракты.", {"leases":1800}, "persistent", incident=50000, combo={"leases":9000}, combo_incident=400000, requires="space_reallocation", cause="customer_churn"),
card("ЗАБРАТЬ WELLNESS-БЮДЖЕТ ЦЕЛИКОМ", "Подписать компании на полноценную wellness-программу конкурента и одновременно убрать потребность в капсулах SleepWork.", "Клиенты уходят в wellness-конкурента.", {"wellness":2800,"leases":1200}, "persistent", combo={"wellness":9000,"leases":7000}, requires="wellness_switch"),
card("ЗАБРАТЬ ДОЛГОСРОЧНЫЕ ДОГОВОРЫ НА КАПСУЛЫ", "Предложить ключевым клиентам более дешёвую долгосрочную аренду у конкурента.", "Долгосрочные договоры SleepWork переходят конкуренту.", {"leases":1800}, "persistent"),
],
"fitmirror": [
card("ВЫВЕСТИ ДЕШЁВЫЙ АНАЛОГ ЗЕРКАЛА", "Запустить домашнее фитнес-устройство с базовыми функциями заметно дешевле FitMirror.", "Покупатели выбирают дешёвый аналог вместо зеркала.", {"hardware":1000}, "temporary", flag="price_pressure"),
card("УВЕСТИ ПОДПИСЧИКОВ В БЕСПЛАТНЫЕ ТРЕНИРОВКИ", "Дать владельцам FitMirror бесплатные программы тренировок без ежемесячной платы.", "Пользователи сокращают платное coaching-сопровождение.", {"coaching":1400}, "temporary", flag="retention_doubt"),
card("ДОКАЗАТЬ, ЧТО ТЕЛЕФОН ЗАМЕНЯЕТ ЗЕРКАЛО", "Провести публичное сравнение FitMirror с тренировкой через обычный смартфон.", "Смартфон воспринимается как замена и снижает обе выручки.", {"hardware":700,"coaching":600}, "temporary", flag="phone_substitute"),
card("ЗАБРАТЬ ЛУЧШИЕ МЕСТА В МАГАЗИНАХ", "Выкупить лучшие демонстрационные позиции у крупных продавцов домашнего фитнеса.", "Зеркала теряют видимость в магазинах.", {"hardware":800}, "temporary"),
card("ПЕРЕМАНИТЬ ПОКУПАТЕЛЕЙ РАССРОЧКОЙ", "Предложить покупателям конкурирующего устройства удобную рассрочку.", "Цена покупки становится главным барьером для FitMirror.", {"hardware":1800}, "persistent", combo={"hardware":3800}, requires="price_pressure", combo_flag="affordability_crisis"),
card("ПЕРЕМАНИТЬ ПОДПИСЧИКОВ БЕЗ ПОТЕРИ ПРОГРЕССА", "Дать перенос истории тренировок, планов и достижений в бесплатный сервис.", "Платные coaching-подписчики уходят без потери прогресса.", {"coaching":2200}, "persistent", combo={"coaching":4800}, requires="retention_doubt", combo_flag="subscription_churn"),
card("ВЫПУСТИТЬ ПОЛНЫЙ АНАЛОГ FITMIRROR НА ТЕЛЕФОНЕ", "Добавить оценку упражнений по камере, персональные планы и вывод тренировки на TV, без покупки зеркала.", "Телефонный аналог заменяет и устройство, и coaching.", {"hardware":1600,"coaching":1200}, "persistent", combo={"hardware":3400,"coaching":2800}, requires="phone_substitute", combo_flag="hardware_substitution"),
card("ВЫТЕСНИТЬ FITMIRROR С ВИТРИН", "Заключить договоры на лучшие витрины магазинов домашнего фитнеса.", "FitMirror теряет торговую видимость.", {"hardware":1200}, "persistent"),
card("ВЫДАВИТЬ FITMIRROR ИЗ ПРОДАЖ ДЕМПИНГОМ", "Предложить устройство заметно дешевле FitMirror во всех ключевых каналах.", "Продажи FitMirror падают из-за демпинга.", {"hardware":2600}, "structural", combo={"hardware":8400}, requires="affordability_crisis"),
card("ЗАПОЛНИТЬ РЫНОК Б/У ЗЕРКАЛАМИ", "Выкупить зеркала у пользователей, уже ушедших с подписки, и массово перепродать их дешевле новых FitMirror.", "Вторичный рынок давит на coaching и поставляет дешёвое железо.", {"coaching":3000}, "structural", combo={"coaching":9200,"hardware":7200}, requires="subscription_churn"),
card("СДЕЛАТЬ ФИТНЕС-ЗЕРКАЛО НЕНУЖНЫМ", "Продвигать полный мобильный фитнес-сервис с камерой телефона и телевизором как прямую замену FitMirror.", "Мобильная замена вытесняет зеркало и coaching.", {"hardware":2400,"coaching":1600}, "structural", combo={"hardware":7800,"coaching":6200}, requires="hardware_substitution"),
card("ЗАБРАТЬ ОСНОВНЫЕ КАНАЛЫ ПРОДАЖ", "Заключить эксклюзивные договоры с основными каналами FitMirror.", "Основные каналы продаж переходят конкуренту.", {"hardware":2000}, "structural"),
],
"cloudkitchen": [
card("ВЫТЕСНИТЬ CLOUDKITCHEN ИЗ ВЫДАЧИ", "Выкупить продвижение конкурирующих кухонь над карточками CloudKitchen в агрегаторах.", "Карточки CloudKitchen теряют заказы в агрегаторах.", {"marketplace":1000}, "temporary", flag="ranking_pressure"),
card("СКУПИТЬ КЛЮЧЕВЫЕ ИНГРЕДИЕНТЫ", "Забрать свободный запас ходовых продуктов у общих поставщиков перед пиковыми днями.", "Дефицит ингредиентов срывает меню и требует расходов.", {"marketplace":800}, "temporary", incident=150000, flag="supply_pressure"),
card("СКОПИРОВАТЬ ХИТЫ МЕНЮ И СБИТЬ ЦЕНУ", "Запустить virtual restaurant с аналогами самых продаваемых блюд CloudKitchen дешевле.", "Клоны меню забирают заказы CloudKitchen.", {"marketplace":1100}, "temporary", flag="menu_clone"),
card("ПЕРЕМАНИТЬ ОФИСЫ БЕСПЛАТНЫМИ ДЕГУСТАЦИЯМИ", "Провести бесплатные дегустации и заключить офисные контракты конкурента.", "Корпоративные заказы сокращаются.", {"corporate":1500}, "temporary"),
card("ЗАБРАТЬ ПРОМО-БЛОКИ АГРЕГАТОРА", "Выкупить лучшие рекламные блоки агрегатора для конкурирующих кухонь.", "CloudKitchen теряет обнаружимость и заказы.", {"marketplace":1800}, "persistent", combo={"marketplace":4000}, requires="ranking_pressure", combo_incident=150000, combo_flag="discovery_crisis"),
card("ПЕРЕХВАТИТЬ ОКНА ПОСТАВОК", "Законтрактовать окна поставок перед пиковыми днями CloudKitchen.", "Меню страдает от дефицита продуктов.", {"marketplace":1600}, "persistent", incident=150000, combo={"marketplace":3800}, combo_incident=300000, requires="supply_pressure", combo_flag="menu_shortage"),
card("ЗАПУСТИТЬ КЛОНЫ БРЕНДОВ С КУПОНАМИ", "Запустить клоны брендов CloudKitchen с купонами и более низкой ценой.", "Клоны подменяют исходные бренды в заказах.", {"marketplace":1900}, "persistent", combo={"marketplace":4200}, requires="menu_clone", combo_flag="brand_substitution"),
card("ЗАБРАТЬ КОРПОРАТИВНЫЕ КОНТРАКТЫ", "Заключить корпоративные договоры вместо CloudKitchen.", "Корпоративная выручка уходит конкуренту.", {"corporate":3000}, "persistent"),
card("ВЫТЕСНИТЬ CLOUDKITCHEN ИЗ ТОПА АГРЕГАТОРА", "Выкупить позиции в топе агрегатора для конкурирующих кухонь.", "CloudKitchen теряет место в выдаче.", {"marketplace":2500}, "structural", combo={"marketplace":8200}, combo_incident=250000, requires="discovery_crisis"),
card("ЗАБРАТЬ КЛИЕНТОВ, ПОКА БЛЮДА СНЯТЫ С МЕНЮ", "Предложить клиентам CloudKitchen замену, пока блюда конкурента сняты с меню.", "Клиенты уходят; это уже customer churn.", {"marketplace":2200}, "structural", incident=100000, combo={"marketplace":7200}, combo_incident=350000, requires="menu_shortage", cause="customer_churn"),
card("ПЕРЕМАНИТЬ ПОСТОЯННЫХ КЛИЕНТОВ К КЛОНАМ МЕНЮ", "Закрепить клиентов CloudKitchen за клонами его меню купонами.", "Постоянные клиенты переходят к клонам.", {"marketplace":2500}, "structural", combo={"marketplace":8000}, requires="brand_substitution"),
card("ЗАКРЕПИТЬ ОФИСЫ ДОЛГОСРОЧНЫМИ ДОГОВОРАМИ", "Заключить эксклюзивные долгосрочные договоры с офисами CloudKitchen.", "Корпоративные контракты закрепляются за конкурентом.", {"corporate":5000}, "structural"),
],
"agrodrone": [
card("ПЕРЕМАНИТЬ ПОКУПАТЕЛЕЙ ОТСРОЧКОЙ ДО УРОЖАЯ", "Предложить покупателям конкурирующих дронов оплату после урожая.", "Продажи оборудования AgroDrone откладываются.", {"equipment":1000}, "temporary", flag="financing_pressure"),
card("СКУПИТЬ СПЕЦИАЛИЗИРОВАННЫЕ КОНТРОЛЛЕРЫ", "Выкупить специализированные контроллеры перед закупкой AgroDrone.", "Поставка оборудования задерживается и требует расходов.", {"equipment":900}, "temporary", incident=150000, flag="component_pressure"),
card("ДАТЬ СПУТНИКОВЫЙ АНАЛИЗ БЕСПЛАТНО", "Предложить фермерам бесплатный спутниковый анализ вместо покупки дрона.", "Фермеры сокращают платный анализ.", {"analysis":1600}, "temporary", flag="satellite_trial"),
card("ПЕРЕМАНИТЬ ПОКУПАТЕЛЕЙ ДЕМО-ДРОНАМИ", "Провести бесплатные демонстрации конкурирующих дронов на ключевых полях.", "Покупатели откладывают заказ AgroDrone.", {"equipment":400}, "temporary"),
card("ПЕРЕТЯНУТЬ ДИЛЕРОВ СЕЗОННЫМ КРЕДИТОМ", "Предложить дилерам сезонный кредит на продажу конкурирующих дронов.", "Дилеры сокращают продажи AgroDrone.", {"equipment":1700}, "persistent", combo={"equipment":3600}, requires="financing_pressure", combo_flag="dealer_financing_loss"),
card("ПЕРЕХВАТИТЬ СЛЕДУЮЩУЮ ПАРТИЮ КОМПЛЕКТУЮЩИХ", "Законтрактовать следующую партию компонентов AgroDrone.", "Производство дронов встаёт и несёт расходы.", {"equipment":1800}, "persistent", incident=150000, combo={"equipment":4000}, combo_incident=300000, requires="component_pressure", combo_flag="production_backlog"),
card("ПРОДАТЬ МОНИТОРИНГ БЕЗ ПОКУПКИ ДРОНА", "Продать фермерским хозяйствам мониторинг как сервис без покупки дрона.", "Сервис заменяет оборудование и часть анализа.", {"analysis":2400,"equipment":1000}, "persistent", combo={"analysis":4800,"equipment":2800}, requires="satellite_trial", combo_flag="service_substitution"),
card("ЗАБРАТЬ РЕГИОНАЛЬНЫЕ ТЕНДЕРЫ", "Подать более выгодные заявки и забрать региональные тендеры AgroDrone.", "Продажи оборудования в регионах сокращаются.", {"equipment":800}, "persistent"),
card("ЗАБРАТЬ КРУПНЫЕ ЗАКАЗЫ ПЕРЕД ПОСЕВНОЙ", "Заключить крупные заказы на дроны перед посевной вместо AgroDrone.", "AgroDrone теряет крупные заказы.", {"equipment":2400}, "structural", combo={"equipment":8000}, requires="dealer_financing_loss"),
card("ЗАБРАТЬ ХОЗЯЙСТВА НА ФОНЕ СРЫВА ПОСТАВОК", "Предложить хозяйствам готовый сервис, пока поставки AgroDrone сорваны.", "Хозяйства уходят; причина переходит в customer churn.", {"equipment":2500,"analysis":1000}, "structural", incident=100000, combo={"equipment":7200,"analysis":3500}, combo_incident=300000, requires="production_backlog", cause="customer_churn"),
card("ЗАМЕНИТЬ ПОКУПКУ ДРОНОВ СЕРВИСОМ ПО ПОДПИСКЕ", "Запустить подписочный мониторинг с камерой и спутниковыми данными вместо покупки дрона.", "Подписка заменяет оборудование и анализ.", {"equipment":2200,"analysis":2000}, "structural", combo={"equipment":7600,"analysis":6500}, requires="service_substitution"),
card("ЗАКРЕПИТЬ ДИЛЕРОВ ЗА КОНКУРЕНТОМ", "Заключить эксклюзивные договоры с дилерами AgroDrone.", "Дилеры закрепляются за конкурентом.", {"equipment":1200}, "structural"),
],
}

CARDS.update({
"moodads": [
card("РАЗОБЛАЧИТЬ СБОР ЭМОЦИОНАЛЬНЫХ ДАННЫХ", "Публично разобрать чувствительные сигналы MoodAds и показать это рекламодателям.", "Рекламодатели сомневаются в приватности и сокращают закупки.", {"saas":800,"analytics":600}, "temporary", rep=-4, flag="privacy_doubt"),
card("ДОБИТЬСЯ ПРОВЕРКИ ДОСТУПА К ДАННЫМ", "Передать партнёрам описание интеграций MoodAds и добиться проверки доступа.", "Проверка ограничивает доступ к данным и снижает продажи.", {"saas":600,"analytics":800}, "temporary", incident=100000, flag="data_access_review"),
card("ДОКАЗАТЬ, ЧТО ТАРГЕТИНГ БЕЗ ЭМОЦИЙ РАБОТАЕТ", "Провести benchmark contextual targeting против MoodAds по цене и конверсии.", "Клиенты видят замену эмоциональному таргетингу.", {"saas":1000,"analytics":400}, "temporary", flag="contextual_proof"),
card("ПЕРЕМАНИТЬ АНАЛИТИЧЕСКИХ КЛИЕНТОВ ДЕШЁВЫМИ ОТЧЁТАМИ", "Предложить клиентам MoodAds более дешёвые аналитические отчёты.", "Аналитические контракты сокращаются.", {"analytics":1400}, "temporary"),
card("ЗАПУСТИТЬ PRIVACY-ПРОВЕРКИ У КЛИЕНТОВ", "Провести privacy-аудиты и предложить клиентам отказаться от рискованных интеграций MoodAds.", "Проверки снижают SaaS и analytics продажи.", {"saas":1400,"analytics":1000}, "persistent", combo={"saas":3200,"analytics":2600}, combo_rep=-8, requires="privacy_doubt", combo_flag="privacy_review_wave"),
card("ДОБИТЬСЯ ОГРАНИЧЕНИЯ ПОТОКА ДАННЫХ", "Добиться у платформ ограничения потока данных для MoodAds.", "Поток данных сужается, а компания несёт расходы.", {"saas":1500,"analytics":1800}, "persistent", incident=100000, combo={"saas":4000,"analytics":5000}, combo_incident=300000, requires="data_access_review", combo_flag="data_restricted"),
card("ПЕРЕВЕСТИ КАМПАНИИ НА ТАРГЕТИНГ БЕЗ ЭМОЦИЙ", "Перевести рекламные кампании клиентов на contextual targeting.", "Кампании уходят с MoodAds.", {"saas":1800,"analytics":800}, "persistent", combo={"saas":3800,"analytics":1800}, requires="contextual_proof", combo_flag="contextual_migration"),
card("ЗАБРАТЬ BI-КОНТРАКТЫ", "Заключить BI-контракты вместо MoodAds.", "Аналитические контракты закрепляются за конкурентом.", {"analytics":2400}, "persistent"),
card("СОРВАТЬ ПРОДЛЕНИЕ ЛИЦЕНЗИЙ ИЗ-ЗА PRIVACY-РИСКА", "Передать клиентам доказательства privacy-риска и предложить замену MoodAds.", "Лицензии не продлеваются.", {"saas":2000,"analytics":1500}, "structural", combo={"saas":7200,"analytics":5000}, combo_rep=-10, requires="privacy_review_wave"),
card("УВЕСТИ КЛИЕНТОВ, ПОКА ТАРГЕТИНГ ОСЛАБ", "Предложить клиентам стабильную альтернативу во время ограничения данных.", "Клиенты уходят; причина становится customer churn.", {"saas":2200,"analytics":1800}, "structural", incident=100000, combo={"saas":8800,"analytics":8000}, combo_incident=700000, requires="data_restricted", cause="customer_churn"),
card("ЗАМЕНИТЬ MOODADS PRIVACY-SAFE АНАЛОГОМ", "Запустить privacy-safe аналог эмоционального таргетинга.", "Privacy-safe сервис заменяет MoodAds.", {"saas":2500,"analytics":1500}, "structural", combo={"saas":7800,"analytics":4500}, requires="contextual_migration"),
card("ЗАКРЕПИТЬ АНАЛИТИКУ У КОНКУРЕНТА", "Заключить эксклюзивные договоры на аналитику клиентов MoodAds.", "Аналитическая выручка уходит конкуренту.", {"analytics":4500}, "structural"),
],
"renteverything": [
card("ЗАБРАТЬ РЕМОНТНЫЕ СЛОТЫ", "Зарезервировать мощности мастерских перед периодом возврата вещей RentEverything.", "Ремонты задерживаются и снижают доступный фонд.", {"rental":700}, "temporary", incident=100000, flag="repair_pressure"),
card("РАСКРУТИТЬ СПОРНЫЕ УДЕРЖАНИЯ", "Собрать реальные спорные случаи с залогами и показать проблему клиентам и владельцам.", "Клиенты и владельцы сомневаются в модели удержаний.", {"rental":400,"commission":500}, "temporary", rep=-3, flag="dispute_attention"),
card("СБИТЬ ЗАЛОГ И ЦЕНУ АРЕНДЫ", "Запустить конкурирующий прокат дешевле и с меньшим залогом.", "Арендаторы выбирают более дешёвый прокат.", {"rental":800}, "temporary", flag="price_pressure"),
card("ПЕРЕМАНИТЬ ВЛАДЕЛЬЦЕВ НУЛЕВОЙ КОМИССИЕЙ", "Предложить владельцам нулевую комиссию за переход в каталог конкурента.", "Комиссионная выручка сокращается.", {"commission":1000}, "temporary"),
card("ОСТАВИТЬ ФОНД БЕЗ БЫСТРОГО РЕМОНТА", "Перехватить ремонтные мощности, необходимые фонду RentEverything.", "Фонд теряет доступность и несёт расходы.", {"rental":1400}, "persistent", incident=100000, combo={"rental":4200}, combo_incident=350000, requires="repair_pressure", combo_flag="inventory_backlog"),
card("ЗАПУСТИТЬ МАССОВУЮ ПРОВЕРКУ СПОРНЫХ УДЕРЖАНИЙ", "Запустить массовые проверки спорных удержаний RentEverything.", "Проверки бьют по аренде и комиссии.", {"rental":800,"commission":1200}, "persistent", incident=80000, combo={"rental":2800,"commission":3800}, combo_incident=300000, combo_rep=-5, requires="dispute_attention", combo_flag="dispute_wave"),
card("ПЕРЕМАНИТЬ АРЕНДАТОРОВ ПОДПИСКОЙ БЕЗ ЗАЛОГА", "Предложить арендаторам подписку конкурента без залога.", "Арендаторы уходят из проката RentEverything.", {"rental":1500}, "persistent", combo={"rental":3800}, requires="price_pressure", combo_flag="renter_churn"),
card("УВЕСТИ ПАРТНЁРСКИЙ КАТАЛОГ", "Предложить владельцам более выгодный партнёрский каталог.", "Комиссионные договоры сокращаются.", {"commission":1800}, "persistent"),
card("ЗАБРАТЬ АРЕНДАТОРОВ, ПОКА ВЕЩИ НА РЕМОНТЕ", "Предложить арендаторам замену, пока вещи RentEverything находятся в ремонте.", "Арендаторы уходят; причина становится customer churn.", {"rental":2000}, "structural", incident=80000, combo={"rental":5500,"commission":1000}, combo_incident=200000, requires="inventory_backlog", cause="customer_churn"),
card("УВЕСТИ ВЛАДЕЛЬЦЕВ И КЛИЕНТОВ НА ФОНЕ СПОРОВ", "Предложить владельцам и клиентам прозрачную альтернативу во время споров.", "Владельцы и клиенты уходят из RentEverything.", {"rental":1500,"commission":1600}, "structural", combo={"rental":6000,"commission":7500}, combo_incident=450000, combo_rep=-8, requires="dispute_wave"),
card("ЗАКРЕПИТЬ АРЕНДАТОРОВ ДЕШЁВОЙ ПОДПИСКОЙ", "Заключить с арендаторами дешёвые долгосрочные подписки конкурента.", "Арендаторы закрепляются у конкурента.", {"rental":2000}, "structural", combo={"rental":7800}, requires="renter_churn"),
card("ЗАКРЕПИТЬ ВЛАДЕЛЬЦЕВ ЭКСКЛЮЗИВНЫМИ УСЛОВИЯМИ", "Заключить эксклюзивные условия с владельцами каталога RentEverything.", "Комиссионная выручка надолго уходит конкуренту.", {"commission":2500}, "structural"),
]})

def main():
    data = json.loads(CATALOG.read_text())
    for item in data["choices"]:
        slug = item["startup_slug"]
        if slug not in CARDS:
            continue
        suffix = item["id"].rsplit("_", 1)[1]
        index = int(suffix) - 1 if suffix.isdigit() else "abcd".index(suffix)
        card_data = CARDS[slug][(item["round_number"] - 1) * 4 + index]
        effect = card_data["effect"]
        effect["group"] = f"{slug}_{'abcd'[index]}"
        attack_types = {
            "sleepwork": ["competition", "competition", "competition", "competition"],
            "fitmirror": ["competition", "competition", "competition", "competition"],
            "cloudkitchen": ["competition", "supply", "competition", "competition"],
            "agrodrone": ["competition", "supply", "competition", "competition"],
            "moodads": ["reputation", "supply", "competition", "competition"],
            "renteverything": ["supply", "reputation", "competition", "competition"],
        }
        item.update({"title": card_data["title"], "short_description": card_data["action"],
                     "result_headline": card_data["title"], "attack_type": attack_types[slug][index],
                     "scene_type": attack_types[slug][index], "weakness_id": None, "weakness_match": "normal",
                     "evidence_fact_ids": [item["evidence_fact_ids"][0]], "target_stream_ids": list(effect["base_effect"]["stream_loss_bps"]),
                     "duration": effect["base_effect"]["duration"], "stack_group": effect["group"],
                     "narrative": {"attack": card_data["action"], "company_response": "Команда оценивает ущерб и выбирает защиту по прогнозу.", "result": card_data["result"]},
                     "v2_effect": effect})
    data["catalog_version"] = "2.0.0"
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

if __name__ == "__main__":
    main()
