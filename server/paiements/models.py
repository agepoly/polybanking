from django.db import models

from configs.models import Config


class Transaction(models.Model):
    """Represent one transation"""

    config = models.ForeignKey(Config)

    reference = models.CharField(max_length=255)
    extra_data = models.TextField(blank=True, null=True)

    amount = models.IntegerField()

    postfinance_id = models.CharField(max_length=255, blank=True, null=True)

    POSTFINANCE_STATUS = (

        ('??', 'Unknow'),
        ('0',  'Invalid or incomplete'),
        ('1',  'Cancelled by customer'),
        ('2',  'Authorisation declined'),
        ('4',  'Order stored'),
        ('40',  'Stored waiting external result'),
        ('41',  'Waiting for client payment'),
        ('5',  'Authorised'),
        ('50',  'Authorized waiting external result'),
        ('51',  'Authorisation waiting'),
        ('52',  'Authorisation not known'),
        ('55',  'Standby'),
        ('56',  'OK with scheduled payments'),
        ('57',  'Not OK with scheduled payments'),
        ('59',  'Authoris. to be requested manually'),
        ('6',  'Authorised and cancelled'),
        ('61',  'Author. deletion waiting'),
        ('62',  'Author. deletion uncertain'),
        ('63',  'Author. deletion refused'),
        ('64',  'Authorised and cancelled'),
        ('7',  'Payment deleted'),
        ('71',  'Payment deletion pending'),
        ('72',  'Payment deletion uncertain'),
        ('73',  'Payment deletion refused'),
        ('74',  'Payment deleted'),
        ('75',  'Deletion handled by merchant'),
        ('8',  'Refund'),
        ('81',  'Refund pending'),
        ('82',  'Refund uncertain'),
        ('83',  'Refund refused'),
        ('84',  'Refund'),
        ('85',  'Refund handled by merchant'),
        ('9',  'Payment requested'),
        ('91',  'Payment processing'),
        ('92',  'Payment uncertain'),
        ('93',  'Payment refused'),
        ('94',  'Refund declined by the acquirer'),
        ('95',  'Payment handled by merchant'),
        ('96',  'Refund reversed'),
        ('99',  'Being processed'),

        )

    postfinance_status = models.CharField(max_length=2, choices=POSTFINANCE_STATUS, default='??')

    INTERNAL_STATUS = (
        ('cr', 'Transation created'),
        ('fw', 'User forwarded to PostFinance'),
        ('fb', 'Feedback from PostFinance'),
    )

    internal_status = models.CharField(max_length=2, choices=INTERNAL_STATUS, default='cr')

    ipn_needed = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_userforwarded_date = models.DateTimeField(blank=True, null=True)
    last_user_back_from_postfinance_date = models.DateTimeField(blank=True, null=True)
    last_postfinance_ipn_date = models.DateTimeField(blank=True, null=True)
    last_ipn_date = models.DateTimeField(blank=True, null=True)

    def amount_chf(self):
        """Return the amount in CHF"""
        return self.amount / 100.0

    def postfinance_status_good(self):
        """Return true if the status of the transaction is good (valid)"""
        return self.postfinance_status in ('5', '9')

    def internal_status_good(self):
        """Return true if the internal status of the transaction if good (user back from postfinance)"""
        return self.internal_status == 'fb'

    def __unicode__(self):
        return self.reference


class TransactionLog(models.Model):
    """A transaction log"""

    transaction = models.ForeignKey(Transaction)
    when = models.DateTimeField(auto_now_add=True)
    extra_data = models.TextField()

    LOG_TYPE = (
        ('created', 'Transaction created'),
        ('userForwarded', 'User forwarded'),
        ('userBackFromPostfinance', 'User back from postfinance'),
        ('postfinanceId', 'Postfinance ID set'),
        ('postfinanceStatus', 'Postfinance status changed'),
        ('ipnfailled', 'IPN Failled'),
        ('ipnsuccess', 'IPN Success'),

        )

    log_type = models.CharField(max_length=64, choices=LOG_TYPE)