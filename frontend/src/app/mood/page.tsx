'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/Button'

export default function MoodPage() {
  const router = useRouter()
  const [selectedMoods, setSelectedMoods] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const moods = [
    { id: 'relaxed', label: 'リラックス', emoji: '😌' },
    { id: 'active', label: 'アクティブ', emoji: '🏃' },
    { id: 'adventure', label: '冒険', emoji: '🎯' },
    { id: 'gourmet', label: 'グルメ', emoji: '🍽️' },
  ]

  const handleMoodToggle = (moodId: string) => {
    setSelectedMoods(prev =>
      prev.includes(moodId)
        ? prev.filter(id => id !== moodId)
        : [...prev, moodId]
    )
  }

  const handleNext = async () => {
    setIsLoading(true)
    // 実際のアプリではここでストアに保存
    await router.push('/conditions')
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        今日の気分を教えてください
      </h1>

      <div className="grid grid-cols-2 gap-4 mb-8">
        {moods.map(mood => (
          <button
            key={mood.id}
            onClick={() => handleMoodToggle(mood.id)}
            className={cn(
              'p-4 rounded-lg border-2 transition-all',
              selectedMoods.includes(mood.id)
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            )}
          >
            <div className="text-3xl mb-2">{mood.emoji}</div>
            <div className="font-medium">{mood.label}</div>
          </button>
        ))}
      </div>

      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={() => router.push('/')}
        >
          戻る
        </Button>
        <Button
          onClick={handleNext}
          disabled={selectedMoods.length === 0}
          isLoading={isLoading}
        >
          次へ
        </Button>
      </div>
    </div>
  )
}

function cn(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}
