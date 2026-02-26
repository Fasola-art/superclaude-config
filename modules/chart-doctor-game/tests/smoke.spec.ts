import { expect, test } from '@playwright/test'

test('quiz flow works', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('quiz-mode')).toBeVisible()

  await page.getByTestId('quiz-up').click()
  await expect(page.getByText('예측:')).toBeVisible()
  await page.getByTestId('quiz-next').click()
  await expect(page.getByTestId('quiz-progress')).toContainText('1/10')
})

test('health mode renders and has pdf button', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('tab-health').click()
  await expect(page.getByTestId('health-mode')).toBeVisible()
  await expect(page.getByTestId('health-score')).toBeVisible()
  await expect(page.getByTestId('health-action')).toBeVisible()
  await expect(page.getByTestId('health-pdf')).toBeVisible()
})

test('news mode plays into boss round and tracks completion text', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('tab-news').click()
  await expect(page.getByTestId('news-mode')).toBeVisible()

  for (let i = 0; i < 6; i += 1) {
    await page.getByTestId('news-dump').click()
  }

  await expect(page.getByTestId('news-round')).toBeVisible()
  await expect(page.getByTestId('news-completion-rate')).toContainText('세션 완료율')
})
