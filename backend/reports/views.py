from django.shortcuts import render
from django.views import View
import pandas as pd

class RevenueView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/revenue.html')
    
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
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
        agg = df.groupby(['نوع دوره']).agg({
                    'کل مبلغ': 'sum',
                    'کل ساعات': 'sum',
                    'ثبت نام شده': 'sum',
                    'کد دوره': 'count'
        }).to_html()
        context = {
            'agg': agg
        }
        return render(request, 'reports/revenue.html', context=context)