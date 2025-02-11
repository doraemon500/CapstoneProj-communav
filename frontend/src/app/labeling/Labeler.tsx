'use client';

import { useSearchParams } from 'next/navigation';
import { Controller, type SubmitHandler, useForm } from 'react-hook-form';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { CATEGORIES } from '@/constants/categories';
import { cn } from '@/lib/utils';
import { type Article } from '@/types';

interface FormData {
  checkedCategories: Record<string, boolean>;
  isVerified: boolean;
}

interface LabelerProps {
  article: Article;
  saved: boolean;
  onSubmit: (articleId: string, categoryIds: number[], isVerified: boolean) => void;
}

export function Labeler(props: LabelerProps) {
  const searchParams = useSearchParams();
  const isVerifyMode = searchParams.get('verify') === 'true';

  const { article, saved, onSubmit } = props;
  const { control, handleSubmit } = useForm<FormData>();

  const onSubmitHandler: SubmitHandler<FormData> = (data) => {
    const categoryIds = Object.entries(data.checkedCategories)
      .filter(([, checked]) => checked)
      .map(([id]) => Number(id));

    onSubmit(article.id, categoryIds, data.isVerified);
  };

  const categoryIds = [article?.category_id];

  return (
    <div key={article.id} className="bg-white shadow-md rounded-lg p-6 mb-4">
      <a href={`https://everytime.kr/370443/v/${article.id}`} target="_blank">
        <h2 className="text-xl font-semibold mb-2">{article.title}</h2>
        <p className="text-gray-600 mb-4">{article.text}</p>
      </a>
      {categoryIds.length > 0 && (
        <div className="flex items-center space-x-2 mb-4">
          {categoryIds.map((categoryId) => {
            const category = CATEGORIES.find((category) => category.id === categoryId);

            if (category) {
              return (
                <Badge key={categoryId} variant="outline">
                  {category.name}
                </Badge>
              );
            }

            return null;
          })}
        </div>
      )}
      <form onSubmit={handleSubmit(onSubmitHandler)}>
        <h3 className="text-lg font-semibold mb-2">Select Categories</h3>
        <div className="space-y-2">
          {CATEGORIES.map((category) => (
            !category.isDeprecated && (
              <div key={category.id} className="flex items-center">
                <Controller
                  control={control}
                  name={`checkedCategories.${category.id}`}
                  render={({ field }) => (
                    <Checkbox
                      id={`category-${category.id}-${article.id}`}
                      className="mr-2"
                      value={category.id}
                      onCheckedChange={field.onChange}
                      checked={field.value}
                    />
                  )}
                />
                <Label htmlFor={`category-${category.id}-${article.id}`}>
                  {category.name}
                </Label>
              </div>
            )
          ))}
        </div>
        <Button
          type="submit"
          className={cn(
            'mt-4',
            saved ? 'bg-green-500 hover:bg-green-600' : ''
          )}
        >
          저장
        </Button>
        {isVerifyMode && (
          <div className="mt-4">
            <Controller
              control={control}
              name="isVerified"
              render={({ field }) => (
                <Checkbox
                  id={`verified-${article.id}`}
                  className="mr-2"
                  onCheckedChange={field.onChange}
                  checked={field.value}
                />
              )}
            />
            <Label htmlFor={`verified-${article.id}`}>검증됨</Label>
          </div>
        )}
      </form>
    </div>
  );
}
