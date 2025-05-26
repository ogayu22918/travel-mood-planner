'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/Button'

export default function ConditionsPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const handleNext = async () => {
    setIsLoading(true)
    await router.push('/areas')
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        詳細を教えてください
      </h1>

      <div className="space-y-6 mb-8">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            人数
          </label>
          <select className="w-full p-2 border border-gray-300 rounded-lg">
            <option>1人</option>
            <option>2人</option>
            <option>3-4人</option>
            <option>5人以上</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            予算
          </label>
          <select className="w-full p-2 border border-gray-300 rounded-lg">
            <option>リーズナブル</option>
            <option>標準</option>
            <option>贅沢</option>
          </select>
        </div>
      </div>

      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={() => router.push('/mood')}
        >
          戻る
        </Button>
        <Button
          onClick={handleNext}
          isLoading={isLoading}
        >
          次へ
        </Button>
      </div>
    </div>
  )
}
