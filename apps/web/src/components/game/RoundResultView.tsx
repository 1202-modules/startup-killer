import React from 'react';
import { motion } from 'framer-motion';
import { RoundResult } from '../../api/types';
import { useGameStore } from '../../stores/gameStore';
import { CashDisplay } from '../ui/CashDisplay';

interface RoundResultViewProps {
  result: RoundResult;
  onContinue: () => void;
  isContinuing?: boolean;
}

const DEFENSE_TITLES: Record<string, string> = {
  none: 'БЕЗ ЗАЩИТЫ', cost_cut: 'СОКРАЩЕНИЕ РАСХОДОВ', cost_cutting: 'СОКРАЩЕНИЕ РАСХОДОВ',
  pr: 'PR-КОНТРАТАКА', supplier_switch: 'СМЕНА ПОСТАВЩИКОВ', pivot: 'ЭКСТРЕННЫЙ ПИВОТ',
  price_war: 'ЦЕНОВАЯ ВОЙНА', price_cut: 'ДЕМПИНГ ЦЕН', legal_threat: 'ЮРИДИЧЕСКАЯ УГРОЗА',
  rebrand: 'СРОЧНЫЙ РЕБРЕНДИНГ', fundraise: 'ПОИСК ИНВЕСТИЦИЙ', product_fix: 'ТЕХНИЧЕСКИЙ ПАТЧ',
  regulatory_defense: 'ЛОББИЗМ И СУДЫ', independent_audit: 'НЕЗАВИСИМЫЙ АУДИТ',
  second_factory: 'ВТОРОЙ ЗАВОД', retention_offer: 'ПРЕДЛОЖЕНИЕ ПОДПИСЧИКАМ',
  campus_redeploy: 'ПЕРЕНОС ТОЧЕК', service_reserve: 'РЕЗЕРВ ОБСЛУЖИВАНИЯ',
  loyalty_program: 'ПРОГРАММА ЛОЯЛЬНОСТИ', sla_guarantee: 'ГАРАНТИЯ СЕРВИСА',
  route_rebuild: 'ПЕРЕСТРОЙКА МАРШРУТОВ', battery_reserve: 'РЕЗЕРВ АККУМУЛЯТОРОВ',
  restaurant_retention: 'УДЕРЖАНИЕ РЕСТОРАНОВ', partner_service: 'ПАРТНЁРСКИЙ СЕРВИС',
  quality_audit: 'АУДИТ КАЧЕСТВА', backup_provider: 'РЕЗЕРВНЫЙ ПРОВАЙДЕР',
  student_retention: 'УДЕРЖАНИЕ УЧЕНИКОВ', school_success_team: 'КОМАНДА ДЛЯ ШКОЛ',
  flexible_lease: 'ГИБКАЯ АРЕНДА', compact_redeploy: 'ПЕРЕНОС КАПСУЛ',
  digital_wellness: 'WELLNESS БЕЗ ОБОРУДОВАНИЯ', price_retention: 'СНИЖЕНИЕ ЦЕНЫ',
  financing_tradein: 'РАССРОЧКА И TRADE-IN', bundled_subscription: 'ПОДПИСКА В КОМПЛЕКТЕ',
  mobile_mode: 'МОБИЛЬНЫЙ РЕЖИМ', retail_buyback: 'ВЫКУП ВИТРИН',
  direct_channel: 'СОБСТВЕННЫЙ КАНАЛ', second_supplier: 'ВТОРОЙ ПОСТАВЩИК',
  unique_menu_loyalty: 'УНИКАЛЬНОЕ МЕНЮ', corporate_retention: 'УДЕРЖАНИЕ КОМПАНИЙ',
  seasonal_leasing: 'СЕЗОННЫЙ ЛИЗИНГ', component_reserve: 'РЕЗЕРВ КОМПОНЕНТОВ',
  drone_as_a_service: 'ДРОНЫ КАК СЕРВИС', dealer_subsidy: 'СУБСИДИЯ ДИЛЕРАМ',
  privacy_safe_mode: 'PRIVACY-SAFE РЕЖИМ', alternative_data: 'ДРУГИЕ ИСТОЧНИКИ ДАННЫХ',
  contextual_mode: 'КОНТЕКСТНЫЙ ТАРГЕТИНГ', analytics_bundle: 'АНАЛИТИКА В ЛИЦЕНЗИИ',
  repair_reserve: 'РЕМОНТНЫЙ РЕЗЕРВ', transparent_insurance: 'ПРОЗРАЧНАЯ СТРАХОВКА',
  lower_deposit: 'СНИЖЕНИЕ ЗАЛОГА', partner_commission_cut: 'СНИЖЕНИЕ КОМИССИИ',
};

export const STREAM_TITLES: Record<string, string> = {
  collars: 'Ошейники', subscription: 'Подписка', kiosks: 'Кофейные точки',
  service: 'Корпоративный сервис', delivery: 'Доставка', maintenance: 'Обслуживание',
  subscriptions: 'Подписки учеников', schools: 'Школьные лицензии',
  leases: 'Аренда капсул', wellness: 'Wellness', hardware: 'Устройства', coaching: 'Тренировки',
  marketplace: 'Заказы', corporate: 'Корпоративные клиенты', equipment: 'Дроны',
  analysis: 'Анализ посевов', saas: 'SaaS', analytics: 'Аналитика',
  rental: 'Аренда вещей', commission: 'Комиссия',
};

const FLAG_TITLES: Record<string, string> = {
  accuracy_doubted: 'сомнения в точности', factory_pressure: 'давление на завод',
  free_alternative: 'бесплатная альтернатива', trust_crisis: 'кризис доверия',
  stockout: 'дефицит устройств', churn_wave: 'отток подписчиков',
  footfall_contested: 'борьба за поток студентов', uptime_exposed: 'известные простои',
  price_pressure: 'ценовое давление', campus_locked: 'потеря кампусных точек',
  repair_backlog: 'очередь ремонтов', margin_squeeze: 'давление на продажи',
  route_scrutiny: 'проверка маршрутов', battery_pressure: 'дефицит аккумуляторов',
  competitor_trial: 'пробный переход ресторанов', route_restricted: 'ограниченные маршруты',
  battery_backlog: 'простои из-за батарей', restaurant_switch: 'переход ресторанов',
  quality_doubt: 'сомнения в качестве', api_pressure: 'нехватка мощности сервиса',
  exam_trial: 'пробный уход учеников', api_bottleneck: 'перебои сервиса',
  cohort_churn: 'отток учеников',
};

export const RoundResultView: React.FC<RoundResultViewProps> = ({ result, onContinue, isContinuing = false }) => {
  const isReducedMotion = useGameStore(s => s.isReducedMotion);
  const defenseType = result.defense?.type?.toLowerCase() || 'none';
  const defenseLabel = DEFENSE_TITLES[defenseType] || defenseType.replace(/_/g, ' ').toUpperCase();
  const deltaColor = (value: number) => value < 0 ? 'text-accent-red' : value > 0 ? 'text-accent-lime' : 'text-text-secondary';

  return (
    <motion.section
      initial={isReducedMotion ? false : { opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="flex min-h-0 flex-1 flex-col gap-3 rounded-2xl border border-border bg-bg-card p-4 shadow-2xl"
    >
      <div className="flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-border/60 pb-2">
        <span className="font-mono text-xs font-bold uppercase tracking-wider text-accent-lime">ИТОГИ РАУНДА {result.round_number}</span>
        <span className="font-mono text-xs text-text-secondary">Месяцы: {result.months_simulated?.join(', ') || 'N/A'}</span>
      </div>

      <div className="grid min-h-0 flex-1 gap-3 xl:grid-cols-2">
        <div className="flex min-w-0 flex-col gap-3">
          <div className="rounded-xl border border-border/50 bg-bg-surface/70 p-3">
            <p className="font-mono text-[11px] uppercase tracking-wider text-text-secondary">ВАША АТАКА</p>
            {result.selected_choice && <h3 className="mt-1 font-display text-sm font-bold text-text-primary">{result.selected_choice.title}</h3>}
            <p className="mt-1 text-xs leading-snug text-text-secondary">{result.selected_choice?.short_description || result.event.title}</p>
          </div>
          <div>
            <p className="font-mono text-[11px] uppercase tracking-wider text-text-secondary">ПОСЛЕДСТВИЯ</p>
            <p className="mt-1 text-xs leading-snug text-text-primary">{result.event.narrative}</p>
          </div>
          {result.defense.company_response && (
            <div className="rounded-xl border border-accent-lime/25 bg-accent-lime/5 p-3">
              <p className="font-mono text-[11px] font-bold uppercase tracking-wider text-accent-lime">ОТВЕТ КОМАНДЫ СТАРТАПА</p>
              <p className="mt-1 text-xs leading-snug text-text-primary">{result.defense.company_response}</p>
            </div>
          )}
          {result.new_circumstance && result.new_circumstance !== result.event.narrative && (
            <div className="rounded-xl border border-accent-lime/25 bg-accent-lime/5 p-3">
              <p className="font-mono text-[11px] font-bold uppercase tracking-wider text-accent-lime">НОВОЕ ОБСТОЯТЕЛЬСТВО</p>
              <p className="mt-1 text-xs leading-snug text-text-secondary">{result.new_circumstance}</p>
            </div>
          )}
        </div>

        <div className="flex min-w-0 flex-col gap-3">
          <div className="rounded-xl border border-border/70 bg-bg-surface p-3">
            <div className="flex flex-wrap items-center justify-between gap-1 font-mono text-[11px]">
              <span className="uppercase text-text-secondary">ЗАЩИТНЫЙ МАНЁВР</span>
              <span className="font-bold text-accent-amber">{defenseLabel}</span>
            </div>
            <p className="mt-1 text-xs leading-snug text-text-primary">{result.defense.summary}</p>
          </div>

          {result.impact && (
            <div className="grid grid-cols-2 gap-x-3 gap-y-1 rounded-xl border border-border/70 bg-bg-surface p-3 text-xs leading-snug text-text-primary">
              <p className="col-span-2 font-mono font-bold text-accent-lime">{result.impact.combo_triggered ? 'КОМБО СРАБОТАЛО' : 'БАЗОВЫЙ ЭФФЕКТ'}</p>
              <p className="col-span-2">Пострадали: {Object.entries(result.impact.affected_streams).map(([id, bps]) => `${STREAM_TITLES[id] || id} −${bps / 100}%`).join(', ')}</p>
              {result.impact.incident_cost_kopeks > 0 && <p className="col-span-2">Разовые расходы: <CashDisplay kopeks={result.impact.incident_cost_kopeks} /></p>}
              <p>Деньги после раунда: <CashDisplay kopeks={result.state_after.cash_kopeks} /></p>
              <p>Без атак к этому месяцу: <CashDisplay kopeks={result.impact.baseline_cash_kopeks} /></p>
              <p className="col-span-2">Дополнительный ущерб от ваших действий: <CashDisplay kopeks={result.impact.player_damage_kopeks} /></p>
              <p className="col-span-2">Выручка: <CashDisplay kopeks={result.state_after.monthly_revenue_kopeks} />; без атак: <CashDisplay kopeks={result.impact.baseline_revenue_kopeks} />; разница: <CashDisplay kopeks={result.impact.revenue_damage_kopeks} /></p>
              <p className="col-span-2">Защита стоила: <CashDisplay kopeks={result.impact.defense_cost_kopeks} />. {result.impact.defense_reason}</p>
              {result.impact.opened_flags.length > 0 && <p className="col-span-2">Открыто для следующего хода: {result.impact.opened_flags.map(flag => FLAG_TITLES[flag] || flag).join(', ')}</p>}
            </div>
          )}

          <div className="grid grid-cols-3 gap-2">
            <div className="min-w-0 rounded-lg bg-bg-surface p-2 text-center">
              <p className="font-mono text-[10px] text-text-secondary">КАЗНА</p>
              <p className={`mt-1 break-words font-mono text-xs font-bold ${deltaColor(result.deltas.cash_kopeks)}`}>
                {result.deltas.cash_kopeks === 0 ? '0 ₽' : <CashDisplay kopeks={result.deltas.cash_kopeks} isChange />}
              </p>
            </div>
            <div className="min-w-0 rounded-lg bg-bg-surface p-2 text-center">
              <p className="font-mono text-[10px] text-text-secondary">ВЫРУЧКА</p>
              <p className={`mt-1 break-words font-mono text-xs font-bold ${deltaColor(result.deltas.monthly_revenue_kopeks)}`}>
                {result.deltas.monthly_revenue_kopeks === 0 ? '0 ₽' : <CashDisplay kopeks={result.deltas.monthly_revenue_kopeks} isChange />}
              </p>
            </div>
            <div className="min-w-0 rounded-lg bg-bg-surface p-2 text-center">
              <p className="font-mono text-[10px] text-text-secondary">РЕПУТАЦИЯ</p>
              <p className={`mt-1 font-mono text-xs font-bold ${deltaColor(result.deltas.reputation)}`}>
                {result.deltas.reputation > 0 ? `+${result.deltas.reputation}` : result.deltas.reputation}
              </p>
            </div>
          </div>
        </div>
      </div>

      <button
        type="button"
        onClick={onContinue}
        disabled={isContinuing}
        className="flex w-full shrink-0 items-center justify-center gap-2 rounded-xl bg-accent-lime px-5 py-3 font-display text-sm font-bold uppercase tracking-wider text-bg-primary transition-all hover:brightness-110 active:scale-[0.99] disabled:opacity-50"
      >
        {isContinuing ? 'Переход к раунду...' : result.game_completed ? 'УЗНАТЬ ИТОГИ ПАРТИИ' : 'ПЕРЕЙТИ К СЛЕДУЮЩЕМУ ХОДУ'}
        {!isContinuing && <span aria-hidden="true" className="font-mono text-base">→</span>}
      </button>
    </motion.section>
  );
};
