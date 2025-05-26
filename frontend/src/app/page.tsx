'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/Button'

export default function HomePage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const handleStartPlanning = async () => {
    setIsLoading(true)
    await router.push('/mood')
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          今日はどんな気分？
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl">
          あなたの気分に合わせて、最適な旅行プランをAIが提案します。
        </p>
        <Button
          size="lg"
          onClick={handleStartPlanning}
          isLoading={isLoading}
          className="text-lg px-8 py-4"
        >
          プランを作成する
        </Button>
      </div>
    </div>
  )
}
