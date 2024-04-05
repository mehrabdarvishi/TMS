from django.shortcuts import render, redirect
from django.views import View
import pandas as pd
import os
from .storage import OverwriteStorage

class RevenueView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        revenue_file_name = 'reports/revenue_report/revenue_report.xlsx'
        if os.path.isfile(revenue_file_name):
            df = pd.read_excel(revenue_file_name)
            df = df[[ 'نام خانوادگي مدرس',
                    'کد دوره',
                    'ثبت نام شده',
                    'کل ساعات',
                    'شماره قرارداد',
                    'نوع دوره',
                    'مسئول دوره',
                    'کل مبلغ',
                    'عنوان دسته بندي دوره',
                    'تاريخ شروع دوره',
                    'تاريخ پايان دوره'
            ]]
            df = df.rename(columns={
                                'نام خانوادگي مدرس': 'مدرس',
                                'عنوان دسته بندي دوره': 'دسته‌بندی دوره',
                                'شماره قرارداد': 'مشتری',
                        })
            df['نفر ساعت'] = df['ثبت نام شده'].multiply(df['کل ساعات'])
            revenue_charts = [
                    {
                        'title': title,
                        'chart':
                        df.groupby([title]).agg({
                            'کل مبلغ': 'sum',
                            'کل ساعات': 'sum',
                            'ثبت نام شده': 'sum',
                            'نفر ساعت': 'sum',
                            'کد دوره': 'count'
                            }).reset_index().rename(columns={
                                'کد دوره': 'تعداد دوره',
                                'کل ساعات': 'مجموع ساعت‌ها',
                                'ثبت نام شده': 'مجموع ثبت‌نام کننده',
                                'نفر ساعت': 'مجموع نفر-ساعت'
                        })
                    }
                for title in  ['مسئول دوره', 'نوع دوره', 'دسته‌بندی دوره', 'مدرس', 'مشتری']
            ]
            '''
            revenue_charts.append(
                    df.agg({
                        'کل مبلغ': 'sum',
                        'کل ساعات': 'sum',
                        'ثبت نام شده': 'sum',
                        'کد دوره': 'count'
                        }).reset_index().rename(columns={
                            'کد دوره': 'تعداد دوره',
                            'کل ساعات': 'مجموع ساعت‌ها',
                            'ثبت نام شده': 'مجموع ثبت‌نام کننده',
                        })
            )
            '''
            for index, revenue_chart in enumerate(revenue_charts):
                revenue_chart['chart']['کل مبلغ'] = revenue_chart['chart']['کل مبلغ'].astype('int64')
                revenue_chart['chart']['مجموع ثبت‌نام کننده'] = revenue_chart['chart']['مجموع ثبت‌نام کننده'].astype('int64')
                revenue_chart['chart']['تعداد دوره'] = revenue_chart['chart']['تعداد دوره'].astype('int64')
                revenue_chart['chart']['مجموع نفر-ساعت'] = revenue_chart['chart']['مجموع نفر-ساعت'].astype('int64')
                revenue_chart['chart']['کل مبلغ'] = revenue_chart['chart']['کل مبلغ'].apply('{:,}'.format)
                revenue_chart['chart']['تعداد دوره'] = revenue_chart['chart']['تعداد دوره'].apply('{:,}'.format)
                revenue_chart['chart']['مجموع ثبت‌نام کننده'] = revenue_chart['chart']['مجموع ثبت‌نام کننده'].apply('{:,}'.format)
                revenue_chart['chart']['مجموع نفر-ساعت'] = revenue_chart['chart']['مجموع نفر-ساعت'].apply('{:,}'.format)
                revenue_charts[index]['chart'] = revenue_chart['chart'].to_html()
                
            context = {
                'revenue_charts': revenue_charts
            }
        return render(request, 'reports/revenue.html', context)
    

class RevenueFileUpdateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/revenue_file_update.html')
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES['excel_file']
        OverwriteStorage(location='reports/revenue_report').save('revenue_report.xlsx', excel_file)
        return redirect('reports:revenue')

