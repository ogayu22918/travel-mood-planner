'use client'

import { Button } from '@/components/ui/Button'

export default function PlansPage() {
  const plans = [
    {
      id: '1',
      title: '渋谷の定番を満喫',
      theme: '人気スポット巡り',
      spots: ['渋谷スクランブルスクエア', '明治神宮', '原宿'],
      budget: '5,000円〜',
    },
    {
      id: '2',
      title: '隠れた名所を探索',
      theme: '穴場スポット中心',
      spots: ['裏渋谷', 'カフェ巡り', 'ギャラリー'],
      budget: '3,000円〜',
    },
  ]

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        あなたにおすすめのプラン
      </h1>

      <div className="grid gap-6">
        {plans.map(plan => (
          <div
            key={plan.id}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
          >
            <h2 className="text-xl font-semibold mb-2">{plan.title}</h2>
            <p className="text-gray-600 mb-4">{plan.theme}</p>
            <div className="flex justify-between items-center">
              <div>
                <div className="text-sm text-gray-500">
                  {plan.spots.join(' → ')}
                </div>
                <div className="text-sm font-medium mt-1">
                  予算: {plan.budget}
                </div>
              </div>
              <Button size="sm">
                詳細を見る
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
