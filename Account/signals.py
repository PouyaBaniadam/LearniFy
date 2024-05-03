from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import Follow, Notification, Wallet


@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        follower = instance.follower
        following = instance.following

        notification = Notification.objects.create(
            title="فالو",
            message=f'<p><a href="/account/profile/{follower.username}"><span style="color:hsl(240,75%,60%);">{follower.username}</span></a> شما را فالو کرد.</p>',
            visibility="PV",
            following=following,
            follower=follower,
            mode="S",
            type="AN",
        )

        notification.users.add(following)
        notification.save()

        if Notification.objects.filter(title="فالو",
                                       message=f'<p><a href="/account/profile/{follower.username}"><span style="color:hsl(240,75%,60%);">{follower.username}</span></a> شما را فالو کرد.</p>',
                                       visibility="PV",
                                       following=following,
                                       follower=follower,
                                       mode="S",
                                       type="AN").count() > 1:
            first_follow_notification = Notification.objects.filter(
                title="فالو",
                message=f'<p><a href="/account/profile/{follower.username}"><span style="color:hsl(240,75%,60%);">{follower.username}</span></a> شما را فالو کرد.</p>',
                visibility="PV",
                following=following,
                follower=follower,
                mode="S",
                type="AN",
            ).first()

            first_follow_notification.delete()

        notification = Notification.objects.create(
            title="فالو",
            message=f'<p>شما <a href="/account/profile/{following.username}"><span style="color:hsl(240,75%,60%);">{following.username}</span></a> را فالو کردید.</p>',
            visibility="PV",
            following=following,
            follower=follower,
            mode="S",
            type="AN",
        )

        notification.users.add(follower)
        notification.save()

        if Notification.objects.filter(
                title="فالو",
                message=f'<p>شما <a href="/account/profile/{following.username}"><span style="color:hsl(240,75%,60%);">{following.username}</span></a> را فالو کردید.</p>',
                visibility="PV",
                following=following,
                follower=follower,
                mode="S",
                type="AN",
        ).count() > 1:
            first_follow_notification = Notification.objects.filter(
                title="فالو",
                message=f'<p>شما <a href="/account/profile/{following.username}"><span style="color:hsl(240,75%,60%);">{following.username}</span></a> را فالو کردید.</p>',
                visibility="PV",
                following=following,
                follower=follower,
                mode="S",
                type="AN",
            ).first()

            first_follow_notification.delete()


@receiver(post_save, sender=Wallet)
def wallet_post_save(sender, instance, created, **kwargs):
    user = instance.user

    if not created:
        if instance.difference > 0:
            formatted_difference = "{:,}".format(instance.difference)
            notification = Notification.objects.create(
                title="شارژ کیف پول",
                message=f'<p>مبلغ <span style="color:hsl(240, 75%, 60%);">{formatted_difference}</span> تومان به کیف پول شما اضافه شد.</p>',
                visibility="PV",
                mode="S",
                type="AN",
            )

            notification.users.add(user)
            notification.save()

        if instance.difference < 0:
            formatted_difference = "{:,}".format(-instance.difference)
            notification = Notification.objects.create(
                title="برداشت از کیف پول",
                message=f'<p>مبلغ <span style="color:hsl(240, 75%, 60%);">{formatted_difference}</span> تومان از حساب شما کسر شد.</p>',
                visibility="PV",
                mode="D",
                type="AN",
            )

            notification.users.add(user)
            notification.save()
