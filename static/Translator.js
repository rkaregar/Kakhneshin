inputs = document.getElementsByTagName('label');
for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].innerText.includes('First name'))
        inputs[i].innerText = 'نام:';
    else if (inputs[i].innerText.includes('Last name'))
        inputs[i].innerText = 'نام خانوادگی:';
    else if (inputs[i].innerText.includes('Gender'))
        inputs[i].innerText = 'جنسیت:';
    else if (inputs[i].innerText.includes('Photo'))
        inputs[i].innerText = 'تصویر:';
    else if (inputs[i].innerText.includes('Username'))
        inputs[i].innerText = 'نام کاربری:';
    else if (inputs[i].innerText.includes('Password1'))
        inputs[i].innerText = 'رمز عبور:';
    else if (inputs[i].innerText.includes('Password2'))
        inputs[i].innerText = 'تکرار رمز عبور:';

    else if (inputs[i].innerText.includes('Email'))
        inputs[i].innerText = 'ایمیل:';
    else if (inputs[i].innerText.includes('Account'))
        inputs[i].innerText = 'شماره حساب:';
    else if (inputs[i].innerText.includes('Phone'))
        inputs[i].innerText = 'شماره تماس:';
    else if (inputs[i].innerText.includes('Role'))
        inputs[i].innerText = 'نقش:';
}

// divs = document.getElementsByTagName('div');
// for (let i = 0; i < inputs.length; i++) {
//     divs[i].innerText = inputs[i].innerText.replace(/Currently/g, 'فعلی');
//     divs[i].innerText = inputs[i].innerText.replace(/Clear/g, 'پاک کردن');
//     divs[i].innerText = inputs[i].innerText.replace(/Change/g, 'تغییر');
//     divs[i].innerText = inputs[i].innerText.replace(/No file chosen/g, 'فایلی انتخاب نشده');
// }

tds = document.getElementsByTagName('td');
for (let i = 0; i < tds.length; i++) {
    if (tds[i].innerText.includes('None'))
        tds[i].innerText = '--';
}


badges = document.getElementsByTagName("span");
for (let i = 0; i < badges.length; i++) {
    badges[i].innerText = badges[i].innerText.replace(/has_breakfast/g, 'صبحانه');
    badges[i].innerText = badges[i].innerText.replace(/has_telephone/g, 'تلفن');
    badges[i].innerText = badges[i].innerText.replace(/has_wifi/g, 'وای‌فای');
    badges[i].innerText = badges[i].innerText.replace(/has_minibar/g, 'مینی‌بار');
    badges[i].innerText = badges[i].innerText.replace(/has_foreign_wc/g, 'توالت فرنگی');
    badges[i].innerText = badges[i].innerText.replace(/has_bath_tub/g, 'وان حمام');
    badges[i].innerText = badges[i].innerText.replace(/has_wc/g, 'توالت');
    badges[i].innerText = badges[i].innerText.replace(/has_shower/g, 'دوش');
}

lis = document.getElementsByTagName('li');
for (let i = 0; i < lis.length; i++) {
    if (lis[i].innerText.includes('Email: This field is req'))
        lis[i].innerText = 'وارد کردن ایمیل اجباری است';
    else if (lis[i].innerText.includes('Account number: This field is required'))
        lis[i].innerText = 'وارد کردن شماره حساب اجباری است';
    else if (lis[i].innerText.includes('Transfer credit: This field is required'))
        lis[i].innerText = 'وارد کردن مقدار انتقالی اجباری است';
    else if (lis[i].innerText.includes('Old password: This field is'))
        lis[i].innerText = 'وارد کردن رمز عبور قبلی اجباری است';
    else if (lis[i].innerText.includes('New password: This field is required'))
        lis[i].innerText = 'وارد کردن رمز عبور جدید اجباری است';
    else if (lis[i].innerText.includes('New password confirmation: This field is required'))
        lis[i].innerText = 'وارد کردن تکرار رمز عبور جدید اجباری است';
    else if (lis[i].innerText.includes('new password: Passwords doesn\'t match'))
        lis[i].innerText = 'رمز عبورهای جدید با یک دیگر برابر نیستند';
    else if (lis[i].innerText.includes('old password: The old password is wrong'))
        lis[i].innerText = 'رمز عبور قبلی اشتباه است';
    else if (lis[i].innerText.includes('نام انگلیسی خدمت: This field is required'))
        lis[i].innerText = 'وارد کردن نام انگلیسی خدمت اجباری است';
    else if (lis[i].innerText.includes('نام فارسی خدمت: This field is require'))
        lis[i].innerText = 'وارد کردن نام فارسی خدمت اجباری است';
    else if (lis[i].innerText.includes('توضیحات خدمت: This field is required'))
        lis[i].innerText = 'وارد کردن توضیحات خدمت اجباری است';
    else if (lis[i].innerText.includes('آدرس عکس خدمت: This field is required'))
        lis[i].innerText = 'وارد کردن آدرس عکس خدمت اجباری است';
    else if (lis[i].innerText.includes('آدرس عکس خدمت: Enter a valid URL'))
        lis[i].innerText = 'آدرس عکس وارد شده معتبر نیست';
    else if (lis[i].innerText.includes('username: There is no user with this username'))
        lis[i].innerText = 'کاربری با نام کاربری وارد شده وجود ندارد';
    else if (lis[i].innerText.includes('Password confirmation: The two password fields didn\'t match'))
        lis[i].innerText = 'رمزهای عبور وارد شده با یک دیگر مطابقت ندارند';
    else if (lis[i].innerText.includes('Email: Enter a valid email address'))
        lis[i].innerText = 'آدرس ایمیل وارد شده معتبر نیست';
    else if (lis[i].innerText.includes('Username: A user with that username already exists'))
        lis[i].innerText = 'نام کاربری وارد شده تکراری است';
    else if (lis[i].innerText.includes('This password is too short. It must contain at least 8 characters'))
        lis[i].innerText = 'رمز عبور وارد شده باید حداقل ۸ کاراکتر بوده و تماما عددی نباشد';
    else if (lis[i].innerText.includes('Password confirmation: This password is too common'))
        lis[i].innerText = 'رمز عبور وارد شده بیش از حد متداول است';
    else if (lis[i].innerText.includes('Password confirmation: This password is entirely numeric'))
        lis[i].innerText = 'رمز عبور وارد شده نمی‌تواند تماما عدد باشد';
    else if (lis[i].innerText.includes('First name: This field is required'))
        lis[i].innerText = 'وارد کردن نام اجباری است';
    else if (lis[i].innerText.includes('Last name: This field is required'))
        lis[i].innerText = 'وارد کردن نام خانوادگی اجباری است';
    else if (lis[i].innerText.includes('Phone number: This field is required'))
        lis[i].innerText = 'وارد کردن شماره تماس اجباری است';
}