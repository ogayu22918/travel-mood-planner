'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/Button'

export default function AreasPage() {
  const router = useRouter()
  const [selectedArea, setSelectedArea] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const areas = [
    { id: 'shibuya', name: '渋谷', description: '若者文化の中心地' },
    { id: 'asakusa', name: '浅草', description: '下町情緒あふれる観光地' },
  ]

  const handleNext = async () => {
    if (!selectedArea) return
    setIsLoading(true)
    await router.push('/plans')
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        おすすめのエリア
      </h1>

      <div className="space-y-4 mb-8">
        {areas.map(area => (
          <button
            key={area.id}
            onClick={() => setSelectedArea(area.id)}
            className={cn(
              'w-full p-4 rounded-lg border-2 text-left transition-all',
              selectedArea === area.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            )}
          >
            <div className="font-semibold text-lg">{area.name}</div>
            <div className="text-gray-600">{area.description}</div>
          </button>
        ))}
      </div>

      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={() => router.push('/conditions')}
        >
          戻る
        </Button>
        <Button
          onClick={handleNext}
          disabled={!selectedArea}
          isLoading={isLoading}
        >
          プランを見る
        </Button>
      </div>
    </div>
  )
}

function cn(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}
