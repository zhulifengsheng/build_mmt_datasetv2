from django.db import models

# create database mmt_databasev1 DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
# python3 manage.py makemigrations --empty annotation
# python3 manage.py makemigrations
# python3 manage.py migrate

# alter table annotation_caption1 auto_increment 1;

# Create your models here.
class Image(models.Model):
    image_name = models.CharField(verbose_name='图片名字', max_length=34, unique=True)

# class UserWorkPoolWithimage(models.Model):
#     pass
    # # 每个用户的索引都是从1开始
    # user_work_pool_index = models.PositiveIntegerField(verbose_name='用户的工作池索引')
    
    # hash_pool_id = models.ForeignKey(verbose_name='随机哈希池的索引', to='RandomHashPoolWithImg', to_field='id', on_delete=models.CASCADE)
    # username = models.ForeignKey(verbose_name='哪个用户的工作池', to='User', to_field='username', on_delete=models.CASCADE)
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['username', 'user_work_pool_index'], name="unique_username_work_pool_index"),
    #     ]

class User(models.Model):
    # dtc 12345
    # fyc fanyvchun
    # hby hbyv
    # IIcce 0123456789
    # lch lv12345
    username = models.CharField(verbose_name='用户名', max_length=5, primary_key=True)
    password = models.CharField(verbose_name='密码', max_length=10)
    
    zh_with_image_working_pool_now = models.PositiveIntegerField(verbose_name='该标注哪个看图片的了', default=0)    # 没有被分配过任务时，初始化为0
    work_total_with_image = models.PositiveSmallIntegerField(verbose_name='计划标注-工作的任务总量')
    start_index_with_image = models.PositiveIntegerField(verbose_name='计划标注-从那个图片开始标注')
    is_admin = models.BooleanField(verbose_name='是否是管理员', default=False)

class Caption(models.Model):
    caption_number = models.PositiveSmallIntegerField(verbose_name='该描述是第几个')    # 1-7
    caption = models.TextField(verbose_name='英文描述')
    caption_ppl = models.CharField(verbose_name='英文描述的PPL值', max_length=5)
    zh_machine_translation = models.TextField(verbose_name='英文描述的机翻', null=True)
    zh_machine_translation_ppl = models.CharField(verbose_name='机翻的PPL值', null=True, max_length=5)
    
    # 在第一阶段结束确定修正后的译文
    zh_without_image_obj = models.OneToOneField(to="ZhWithoutImage", to_field="id", on_delete=models.SET_NULL, null=True)

    # 在第二阶段结束确定修正后的译文
    fix_zh_with_image_obj = models.OneToOneField(to="FixZhWithImage", to_field="id", on_delete=models.SET_NULL, null=True)

    image_obj = models.ForeignKey(to="Image", to_field="id", on_delete=models.CASCADE)    # 链接到那个图片
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['image_obj', 'caption_number'], name="this_image's_unique_caption"),
        ]

class ZhWithoutImage(models.Model):
    user_thinks_caption_ambiguity = models.BooleanField(verbose_name='是否歧义', default=False)
    correct_number = models.PositiveSmallIntegerField(verbose_name='正确的那个中文的序号', default=0)
    # 歧义句的多个译文用'\n'分割
    zhs_without_image = models.TextField(verbose_name='不看图片标注的中文译文')
    # 多个PPL值用空格分割, 最多4个
    zhs_without_image_ppl = models.CharField(verbose_name='该中文译文的PPL值', max_length=23)

    user_that_annots_it = models.ForeignKey(to="User", to_field="username", on_delete=models.SET_NULL, null=True)
    caption_id = models.PositiveIntegerField(verbose_name='该修正是对哪个英文描述修正的')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_that_annots_it', 'caption_id'], 
                name="user_annot_caption_only_once"),
        ]

class FixZhWithImage(models.Model):
    fix_zh_with_image = models.TextField(verbose_name='对不看图片标注的中文译文fix之后的结果')

    zh_with_image = models.TextField(verbose_name='看图片标注的中文译文', null=True)
    zh_with_image_ppl = models.CharField(verbose_name='该中文译文的PPL值', max_length=5, null=True)
    
    user_that_fixs_and_annots_it = models.ForeignKey(to="User", to_field="username", on_delete=models.SET_NULL, null=True)
    caption_id = models.PositiveIntegerField(verbose_name='该修正是对哪个英文描述修正的')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_that_fixs_and_annots_it', 'caption_id'], 
                name="user_fix_and_annot_zh_only_once"),
        ]

class FixInfo(models.Model):
    # 位置从0开始
    start_pos = models.PositiveSmallIntegerField(verbose_name='该修正在中文中开始的位置')
    end_pos = models.PositiveSmallIntegerField(verbose_name='该修正在中文中结束的位置')
    
    error_choices = (
        (1, '名词'), (2, '动词'), (3, '形容词'),
        (4, '数量'), (5, '其他错误'), (6, '描述细化'),
    )
    which_classification = models.PositiveSmallIntegerField(verbose_name='哪个修正类型', choices=error_choices)
    word_before_change = models.CharField(max_length=50)
    word_after_change = models.CharField(max_length=50)
    
    fix_zh_that_belongs_to = models.ForeignKey(to="FixZhWithImage", to_field="id", on_delete=models.CASCADE)
    # 不做外键，本身是为了方便统计信息所用
    username = models.CharField(verbose_name='用户名', max_length=5)