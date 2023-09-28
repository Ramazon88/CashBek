import random
import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from simple_history.models import HistoricalRecords
from apps.users.manager import UserManager

USER = 'user'
SELLER = 'seller'
VENDOR = 'vendor'
MANAGER = 'manager'

USER_TYPES = (
    (USER, _("User"),),
    (VENDOR, _("Vendor"),),
    (MANAGER, _("Manager"),),
    (SELLER, _("Seller"),)
)
NEW, CODE_VERIFIED, HALF, DONE = (
    "new",
    "code_verified",
    "half_done",
    "done"
)

AUTH_STATUS = (
    (NEW, _("New")),
    (CODE_VERIFIED, _("Code verified")),
    (HALF, _("Done without MyID")),
    (DONE, _("Done"))
)

REGION = (
    ('03', 'АНДИЖОН ВИЛОЯТИ'),
    ('06', 'БУХОРО ВИЛОЯТИ'),
    ('08', 'ЖИЗЗАХ ВИЛОЯТИ'),
    ('10', 'КАШКАДАРЁ ВИЛОЯТИ'),
    ('12', 'НАВОИЙ ВИЛОЯТИ'),
    ('14', 'НАМАНГАН ВИЛОЯТИ'),
    ('18', 'САМАРКАНД ВИЛОЯТИ'),
    ('22', 'СУРХОНДАРЁ ВИЛОЯТИ'),
    ('24', 'СИРДАРЁ ВИЛОЯТИ'),
    ('26', 'ТОШКЕНТ ШАХРИ'),
    ('27', 'ТОШКЕНТ ВИЛОЯТИ'),
    ('30', 'ФАРГОНА ВИЛОЯТИ'),
    ('33', 'ХОРАЗМ ВИЛОЯТИ'),
    ('35', 'КОРАКАЛПОГИСТОН РЕСПУБЛИКАСИ')
)

DISTRICT = (
    ('001', 'АНДИЖОН ШАХРИ'),
    ('002', 'АСАКА ШАХРИ'),
    ('003', 'ХОНОБОД ШАХРИ'),
    ('004', 'КОРАСУВ ШАХРИ'),
    ('005', 'Г.ШАХРИХАН'),
    ('006', 'АНДИЖОН ТУМАНИ'),
    ('007', 'АСАКА ТУМАНИ'),
    ('008', 'БАЛИКЧИ ТУМАНИ'),
    ('009', 'БУЗ ТУМАНИ'),
    ('010', 'БУЛОКБОШИ ТУМАНИ'),
    ('011', 'ЖАЛОЛКУДУК ТУМАНИ'),
    ('012', 'ИЗБОСКАН ТУМАНИ'),
    ('013', 'КОМСОМОЛАБАДСКИЙ'),
    ('014', 'КУРГОНТЕПА ТУМАНИ'),
    ('015', 'МАРХАМАТ ТУМАНИ'),
    ('016', 'ОЛТИНКУЛ ТУМАНИ'),
    ('017', 'ПАХТАОБОД ТУМАНИ'),
    ('018', 'ХУЖАОБОД ТУМАНИ'),
    ('210', 'УЛУГНОР ТУМАНИ'),
    ('214', 'ШАХРИХОН ТУМАНИ'),
    ('019', 'ОЛОТ ТУМАНИ'),
    ('020', 'ВОБКЕНТ ТУМАНИ'),
    ('021', 'ГИЖДУВОН ТУМАНИ'),
    ('022', 'БУХОРО ТУМАНИ'),
    ('023', 'КОРАКУЛ ТУМАНИ'),
    ('024', 'РОМИТАН ТУМАНИ'),
    ('025', 'ЖОНДОР ТУМАНИ'),
    ('026', 'ШОФИРКОН ТУМАНИ'),
    ('027', 'ПЕШКУ ТУМАНИ'),
    ('028', 'КОРОВУЛБОЗОР ТУМАНИ'),
    ('029', 'КОГОН ТУМАНИ'),
    ('030', 'БУХОРО ШАХРИ'),
    ('220', 'КОГОН ШАХРИ'),
    ('031', 'ЖИЗЗАХ ШАХРИ'),
    ('032', 'ПАХТАКОР ТУМАНИ'),
    ('033', 'ГАЛЛАОРОЛ ТУМАНИ'),
    ('034', 'ДУСТЛИК ТУМАНИ'),
    ('035', 'МИРЗАЧУЛ ТУМАНИ'),
    ('036', 'ЗОМИН ТУМАНИ'),
    ('037', 'БАХМАЛ ТУМАНИ'),
    ('038', 'ФОРИШ ТУМАНИ'),
    ('039', 'ЗАФАРОБОД ТУМАНИ'),
    ('040', 'ШАРОФ РАШИДОВ ТУМАНИ'),
    ('041', 'АРНАСОЙ ТУМАНИ'),
    ('042', 'ЗАРБДОР ТУМАНИ'),
    ('217', 'ЯНГИОБОД ТУМАНИ'),
    ('043', 'КАРШИ ШАХРИ'),
    ('044', 'КАРШИ ТУМАНИ'),
    ('045', 'ГУЗОР ТУМАНИ'),
    ('046', 'ДЕХКОНОБОД ТУМАНИ'),
    ('047', 'КАМАШИ ТУМАНИ'),
    ('048', 'КОСОН ТУМАНИ'),
    ('049', 'ШАХРИСАБЗ ШАХРИ'),
    ('050', 'ЧИРОКЧИ ТУМАНИ'),
    ('051', 'ЯККАБОГ ТУМАНИ'),
    ('052', 'КИТОБ ТУМАНИ'),
    ('053', 'КАСБИ ТУМАНИ'),
    ('054', 'НИШОН ТУМАНИ'),
    ('055', 'У.ЮСУПОВСКИЙ'),
    ('056', 'МУБОРАК ТУМАНИ'),
    ('057', 'БАХОРИСТАНСКИЙ'),
    ('213', 'ШАХРИСАБЗ ТУМАНИ'),
    ('221', 'МИРИШКОР ТУМАНИ'),
    ('058', 'НАВОИЙ ШАХРИ'),
    ('059', 'ЗАРАФШОН ШАХРИ'),
    ('060', 'Г.УЧКУДУК'),
    ('061', 'КАРМАНА ТУМАНИ'),
    ('062', 'КОНИМЕХ ТУМАНИ'),
    ('063', 'КИЗИЛТЕПА ТУМАНИ'),
    ('064', 'НАВБАХОР ТУМАНИ'),
    ('065', 'НУРОТА ТУМАНИ'),
    ('066', 'ХАТИРЧИ ТУМАНИ'),
    ('067', 'ТОМДИ ТУМАНИ'),
    ('211', 'УЧКУДУК ТУМАНИ'),
    ('224', 'ГОЗГОН ШАХРИ'),
    ('068', 'НАМАНГАН ШАХРИ'),
    ('069', 'МИНГБУЛОК ТУМАНИ'),
    ('070', 'КОСОНСОЙ ТУМАНИ'),
    ('071', 'НОРИН ТУМАНИ'),
    ('072', 'ПОП ТУМАНИ'),
    ('073', 'ТУРАКУРГОН ТУМАНИ'),
    ('074', 'УЙЧИ ТУМАНИ'),
    ('075', 'УЧКУРГОН ТУМАНИ'),
    ('076', 'ЧУСТ ТУМАНИ'),
    ('077', 'ЯНГИКУРГОН ТУМАНИ'),
    ('078', 'НАМАНГАН ТУМАНИ'),
    ('079', 'ЧОРТОК ТУМАНИ'),
    ('080', 'ОКДАРЁ ТУМАНИ'),
    ('081', 'БУЛУНГУР ТУМАНИ'),
    ('082', 'ГУЗАЛКЕНТСКИЙ'),
    ('083', 'ЖОМБОЙ ТУМАНИ'),
    ('084', 'ИШТИХОН ТУМАНИ'),
    ('085', 'КАТТАКУРГОН ТУМАНИ'),
    ('086', 'КУШРАБОТ ТУМАНИ'),
    ('087', 'НАРПАЙ ТУМАНИ'),
    ('088', 'НУРОБОД ТУМАНИ'),
    ('089', 'ПАСТДАРГОМ ТУМАНИ'),
    ('090', 'ПАХТАЧИ ТУМАНИ'),
    ('091', 'ПАЙАРИК ТУМАНИ'),
    ('092', 'САМАРКАНД ТУМАНИ'),
    ('093', 'ТАЙЛОК ТУМАНИ'),
    ('094', 'УРГУТ ТУМАНИ'),
    ('095', 'ЧЕЛЕКСКИЙ'),
    ('096', 'САМАРКАНД ШАХРИ'),
    ('097', 'КАТТАКУРГОН ШАХРИ'),
    ('215', 'ТЕМИРЮЛЬСКИЙ'),
    ('218', 'Г.АКТАШ'),
    ('219', 'Г.УРГУТ'),
    ('098', 'ТЕРМИЗ ШАХРИ'),
    ('099', 'БОЙСУН ТУМАНИ'),
    ('100', 'ДЕНОВ ТУМАНИ'),
    ('101', 'ЖАРКУРГОН ТУМАНИ'),
    ('102', 'МУЗРАБОТ ТУМАНИ'),
    ('103', 'ШЕРОБОД ТУМАНИ'),
    ('104', 'ШУРЧИ ТУМАНИ'),
    ('105', 'УЗУН ТУМАНИ'),
    ('106', 'САРИОСИЁ ТУМАНИ'),
    ('107', 'АНГОР ТУМАНИ'),
    ('108', 'КИЗИРИК ТУМАНИ'),
    ('109', 'КУМКУРГОН ТУМАНИ'),
    ('110', 'ТЕРМИЗ ТУМАНИ'),
    ('111', 'ОЛТИНСОЙ ТУМАНИ'),
    ('112', 'БАНДИХОН ТУМАНИ'),
    ('113', 'Г.БАХТ'),
    ('114', 'ГУЛИСТОН ШАХРИ'),
    ('115', 'ЯНГИЕР ШАХРИ'),
    ('116', 'ШИРИН ШАХРИ'),
    ('117', 'Г.СЫРДАРЬЯ'),
    ('118', 'ОКОЛТИН ТУМАНИ'),
    ('119', 'БОЁВУТ ТУМАНИ'),
    ('120', 'ГУЛИСТОН ТУМАНИ'),
    ('121', 'САРДОБА ТУМАНИ'),
    ('122', 'СИРДАРЁ ТУМАНИ'),
    ('123', 'САЙХУНОБОД ТУМАНИ'),
    ('124', 'ХАВАСТ ТУМАНИ'),
    ('125', 'МЕХНАТАБАДСКИЙ'),
    ('126', 'МИРЗАОБОД ТУМАНИ'),
    ('197', 'ТОШКЕНТ ШАХРИ'),
    ('198', 'УЧТЕПА ТУМАНИ'),
    ('199', 'БЕКТЕМИР ТУМАНИ'),
    ('200', 'ЮНУСОБОД ТУМАНИ'),
    ('201', 'МИРЗО УЛУГБЕК ТУМАНИ'),
    ('202', 'МИРОБОД ТУМАНИ'),
    ('203', 'ШАЙХОНТОХУР ТУМАНИ'),
    ('204', 'ОЛМАЗОР ТУМАНИ'),
    ('205', 'СИРГАЛИ ТУМАНИ'),
    ('227', 'ЯНГИХАЁТ ТУМАНИ'),
    ('206', 'ЯККАСАРОЙ ТУМАНИ'),
    ('207', 'ЯШНОБОД ТУМАНИ'),
    ('208', 'ЧИЛОНЗОР ТУМАНИ'),
    ('127', 'ОХАНГАРОН ШАХРИ'),
    ('128', 'ОЛМАЛИК ШАХРИ'),
    ('129', 'АНГРЕН ШАХРИ'),
    ('130', 'БЕКОБОД ШАХРИ'),
    ('131', 'ЧИРЧИК ШАХРИ'),
    ('132', 'ОККУРГОН ТУМАНИ'),
    ('133', 'ОХАНГАРОН ТУМАНИ'),
    ('134', 'БУСТОНЛИК ТУМАНИ'),
    ('135', 'БУКА ТУМАНИ'),
    ('136', 'ЗАНГИОТА ТУМАНИ'),
    ('137', 'БЕКОБОД ТУМАНИ'),
    ('138', 'КИБРАЙ ТУМАНИ'),
    ('139', 'ПАРКЕНТ ТУМАНИ'),
    ('140', 'КУЙИЧИРЧИК ТУМАНИ'),
    ('141', 'ПСКЕНТ ТУМАНИ'),
    ('142', 'ТОШКЕНТ ТУМАНИ'),
    ('143', 'УРТАЧИРЧИК ТУМАНИ'),
    ('144', 'ЧИНОЗ ТУМАНИ'),
    ('145', 'ЮКОРИЧИРЧИК ТУМАНИ'),
    ('146', 'ЯНГИЙУЛ ТУМАНИ'),
    ('147', 'ЯНГИЙУЛ ШАХРИ'),
    ('223', 'НУРАФШОН ШАХРИ'),
    ('148', 'КУКОН ШАХРИ'),
    ('149', 'МАРГИЛОН ШАХРИ'),
    ('150', 'ФАРГОНА ШАХРИ'),
    ('151', 'КУВАСОЙ ШАХРИ'),
    ('152', 'БЕШАРИК ТУМАНИ'),
    ('153', 'БОГДОД ТУМАНИ'),
    ('154', 'БУВАЙДА ТУМАНИ'),
    ('155', 'ДАНГАРА ТУМАНИ'),
    ('156', 'ЁЗЁВОН ТУМАНИ'),
    ('157', 'КУВА ТУМАНИ'),
    ('158', 'ОЛТИАРИК ТУМАНИ'),
    ('159', 'КУШТЕПА ТУМАНИ'),
    ('160', 'РИШТОН ТУМАНИ'),
    ('161', 'СУХ ТУМАНИ'),
    ('162', 'ТОШЛОК ТУМАНИ'),
    ('163', 'УЗБЕКИСТОН ТУМАНИ'),
    ('164', 'УЧКУПРИК ТУМАНИ'),
    ('165', 'ФАРГОНА ТУМАНИ'),
    ('166', 'ФУРКАТ ТУМАНИ'),
    ('167', 'КИРГУЛИЙСКИЙ'),
    ('168', 'УРГАНЧ ШАХРИ'),
    ('169', 'ХИВА ШАХРИ'),
    ('170', 'ПИТНАК ШАХРИ'),
    ('171', 'ГУРЛАН ТУМАНИ'),
    ('172', 'БОГОТ ТУМАНИ'),
    ('173', 'ХАЗОРАСП ТУМАНИ'),
    ('174', 'ХОНКА ТУМАНИ'),
    ('175', 'ЯНГИАРИК ТУМАНИ'),
    ('176', 'КУШКУПИР ТУМАНИ'),
    ('177', 'ШОВОТ ТУМАНИ'),
    ('178', 'УРГАНЧ ТУМАНИ'),
    ('179', 'ЯНГИБОЗОР ТУМАНИ'),
    ('212', 'ХИВА ТУМАНИ'),
    ('226', 'ТУПРОККАЛЪА ТУМАНИ'),
    ('180', 'НУКУС ШАХРИ'),
    ('181', 'ТАХИАТОШ ШАХРИ'),
    ('182', 'КЕГЕЙЛИ ТУМАНИ'),
    ('183', 'ШУМАНАЙ ТУМАНИ'),
    ('184', 'КУНГИРОТ ТУМАНИ'),
    ('185', 'МУЙНОК ТУМАНИ'),
    ('186', 'АКМАНГИТСКИЙ'),
    ('187', 'ТАХТАКУПИР ТУМАНИ'),
    ('188', 'ТУРТКУЛ ТУМАНИ'),
    ('189', 'ХУЖАЙЛИ ТУМАНИ'),
    ('190', 'ЧИМБОЙ ТУМАНИ'),
    ('191', 'БЕРУНИЙ ТУМАНИ'),
    ('192', 'КОНЛИКУЛ ТУМАНИ'),
    ('193', 'КОРАУЗАК ТУМАНИ'),
    ('194', 'ЭЛЛИККАЛА ТУМАНИ'),
    ('195', 'БОЗАТАУССКИЙ'),
    ('196', 'МАНГИТСКИЙ'),
    ('209', 'АМУДАРЁ ТУМАНИ'),
    ('216', 'НУКУС ТУМАНИ'),
    ('222', 'ТАХИАТОШ ТУМАНИ'),
    ('225', 'БУЗАТОВ ТУМАНИ')
)


class UserConfirmation(models.Model):
    code = models.CharField(max_length=10)
    user = models.ForeignKey('users.User', models.CASCADE, 'verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        self.expiration_time = timezone.now() + timedelta(minutes=2)
        super(UserConfirmation, self).save(*args, **kwargs)


class User(AbstractUser):
    _validate_phone = RegexValidator(
        regex=r"^(!?){0}([998]){3}([3-9]){1}([0-9]){1}([0-9]){7}$",
        message=_("Your phone number must start with 9 and not exceed 12 characters. For example: 998993451545"),
    )
    """
    To store users
    """

    phone = models.CharField(
        _('phone'),
        max_length=150,
        unique=True,
        help_text=_('Required. Enter valid phone number.'),
        error_messages={
            'unique': _("A user with that phone already exists."),
        },
        validators=[_validate_phone]
    )
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    user_type = models.CharField(max_length=60, choices=USER_TYPES, default=USER)
    auth_status = models.CharField(max_length=60, choices=AUTH_STATUS, default=NEW)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    simple_user = models.OneToOneField("SimpleUsers", on_delete=models.CASCADE, null=True, related_name="simple_user")
    vendor = models.OneToOneField("Vendor_account", on_delete=models.CASCADE, null=True, related_name="vendors")
    seller = models.OneToOneField("Seller", on_delete=models.CASCADE, null=True, related_name="seller")
    manager = models.OneToOneField("Manager", on_delete=models.CASCADE, null=True, related_name="manager")
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(6)])  # 493649
        UserConfirmation.objects.create(
            user_id=self.pk,
            code=code
        )
        return code

    def create_verify_code_demo(self):
        code = "030303"  # 493649
        UserConfirmation.objects.create(
            user_id=self.pk,
            code=code
        )
        return code

    def check_username(self):
        if not self.username:
            self.username = self.phone

    def check_pass(self):
        if not self.password:
            temp_password = f"password{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_pass()
        self.hashing_password()
        self.check_username()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def is_dashboard(self):
        if self.user_type in [VENDOR, MANAGER] and self.is_active:
            return True
        return False

    def is_manager(self):
        if self.user_type in [MANAGER] and self.is_active:
            return True
        return False

    def __str__(self):
        return self.get_full_name() or self.get_username()


class SimpleUsers(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
    first_name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
    last_name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    passport_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Номер паспорта")
    doc_type_id = models.CharField(max_length=100, null=True, blank=True)
    doc_type = models.CharField(max_length=512, null=True, blank=True, verbose_name="Тип документа")
    doc_expiry_date = models.CharField(max_length=100, null=True, blank=True)
    doc_issued_by = models.CharField(max_length=256, null=True, blank=True)
    doc_issued_by_id = models.CharField(max_length=256, null=True, blank=True)
    doc_type_id_cbu = models.CharField(max_length=256, null=True, blank=True)
    doc_issued_date = models.CharField(max_length=256, null=True, blank=True)
    citizenship = models.CharField(max_length=100, null=True, blank=True, verbose_name="Гражданство")
    citizenship_id = models.CharField(max_length=100, null=True, blank=True)
    citizenship_id_cbu = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True, verbose_name="Национальность")
    nationality_id = models.CharField(max_length=100, null=True, blank=True)
    nationality_id_cbu = models.CharField(max_length=100, null=True, blank=True)
    birth_country = models.CharField(max_length=100, null=True, blank=True)
    birth_country_id = models.CharField(max_length=100, null=True, blank=True)
    birth_country_id_cbu = models.CharField(max_length=100, null=True, blank=True)
    birth_place = models.CharField(max_length=100, null=True, blank=True, verbose_name="Место рождения")
    sdk_hash = models.CharField(max_length=256, null=True, blank=True)
    pinfl = models.CharField(max_length=100, unique=True, null=True, blank=True, error_messages={
        'unique': _("A user with that pinfl already exists."),
    }, verbose_name="ПИНФЛ")
    photo = models.ImageField(upload_to="user/", null=True, blank=True, )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=100, null=True, blank=True, verbose_name="Пол")
    region = models.CharField(max_length=100, null=True, blank=True, verbose_name="Значение региона")
    region_id = models.CharField(max_length=100, null=True, blank=True)
    region_id_cbu = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True, verbose_name="Значение района (города)")
    district_id = models.CharField(max_length=100, null=True, blank=True)
    district_id_cbu = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True, verbose_name="Адрес")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Обычные пользователи"
        verbose_name_plural = "Обычные пользователи"


class Vendor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании", unique=True)
    type_of_activity = models.CharField(max_length=100, verbose_name="Тип активности")
    price = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(10)])
    logo = models.ImageField(upload_to='vendor/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"


class Seller(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя организация")
    seller_name = models.CharField(max_length=100, verbose_name="Имя продавца")
    telegram_id = models.CharField(max_length=100, unique=True, verbose_name="Telegram ID")
    legal_entity_name = models.CharField(max_length=100, verbose_name="Наименования юридического лица")
    legal_entity_address = models.CharField(max_length=512, verbose_name="Адрес юридического лица")
    inn = models.CharField(max_length=512, verbose_name="СТИР")
    bank = models.CharField(max_length=512, verbose_name="Юридическое лицо банк")
    mfo = models.CharField(max_length=512, verbose_name="МФО")
    schot = models.CharField(max_length=512, verbose_name="Р/С")
    name_shef = models.CharField(max_length=512, verbose_name="Контактное лицо(Ф.И.О)")
    region = models.CharField(max_length=100, verbose_name="Область", choices=REGION)
    district = models.CharField(max_length=100, verbose_name="Район", choices=DISTRICT)

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"


    # def total(self):

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя Менеджер")
    telegram_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="Telegram ID")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self):
        return self.name


class Vendor_account(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя сотрудника")
    telegram_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="Telegram ID")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name="Vendor", related_name="vendor")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Vendor account"
        verbose_name_plural = "Vendor accounts"
