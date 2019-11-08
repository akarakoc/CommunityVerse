from django.db import models


class Primitives(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter your primitive data types')
    def __str__(self):
        return self.name

class communityUsers(models.Model):
    nickName = models.CharField(max_length=200, null=True, help_text='Enter your nickname')	
    userName = models.CharField(max_length=200, null=True, help_text='Enter your username')	
    userSurname = models.CharField(max_length=200, null=True, help_text='Enter your surname')		
    userMail = models.EmailField()	
    userPassword = models.CharField(max_length=200, null=True, help_text='Enter your password')	
    creationDate = models.DateTimeField(null=True)	
    communityPoint = models.CharField(max_length=200, null=True, help_text='Community Point')	
    userPhoto = models.CharField(max_length=200, null=True, help_text='Community Point')
    def __str__(self):        
        return self.nickName	



class Communities(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter community name')
    description = models.CharField(max_length=200, null=True, help_text='Enter community description')	
    communityHash = models.CharField(max_length=200, null=True, help_text='Enter community hash')	
    communityPrv = models.CharField(max_length=200, null=True, help_text='community private or not')	
    communityPhoto = models.CharField(max_length=200, null=True, help_text='community photo')	
    communityPopularity = models.CharField(max_length=200, null=True, help_text='community private or not')
    communityCreator = models.ForeignKey(communityUsers, related_name='creator',on_delete=models.SET_NULL, null=True)
    communityMembers = models.ManyToManyField(communityUsers, related_name='members', help_text='Select members')
    communityCreationDate= models.DateTimeField(null=True)	
    def __str__(self):
        return self.name

class Datatypes(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter ypur datatype') 
    datatypeCreator = models.ForeignKey(communityUsers, related_name='datatypecreator',on_delete=models.SET_NULL, null=True)
    relatedCommunity = models.ForeignKey(Communities, related_name='relcommunity',help_text='Select related community',on_delete=models.SET_NULL, null=True)
    datatypeCreationDate= models.DateTimeField(null=True)
    datatypePhoto = models.CharField(max_length=200, null=True, help_text='datatype photo')
    def __str__(self):
        return self.name
		
class DatatypeFields(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter ypur datatype')
    relatedDatatype = models.ForeignKey(Datatypes, help_text='Select related datatype', on_delete=models.SET_NULL, null=True)
    relatedComm = models.ForeignKey(Communities, help_text='Select related datatype', on_delete=models.SET_NULL, null=True)
    fieldCreator = models.ForeignKey(communityUsers, related_name='fieldsCreator',on_delete=models.SET_NULL, null=True)
    fieldCreationDate= models.DateTimeField(null=True)
    fieldRequired = models.BooleanField(default=False)
    fronttableShow = models.BooleanField(default=False)
    relatedPrimitives = models.ForeignKey(Primitives, help_text='Select related primitive', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name  
    
     
class Posts(models.Model):
    relatedCommunityforPost = models.ForeignKey(Communities, related_name='postCommunity',on_delete=models.SET_NULL, null=True)
    relatedDatatypes = models.ForeignKey(Datatypes, related_name='relatedDatatype',on_delete=models.SET_NULL, null=True)
    entryHash = models.CharField(max_length=200, null=True, help_text='Enter name of type')
    propertyName = models.CharField(max_length=200, null=True, help_text='Enter name of type')
    propertyValue = models.CharField(max_length=200, null=True, help_text='Enter name of type')
    postCreator = models.ForeignKey(communityUsers, related_name='postcreator',on_delete=models.SET_NULL, null=True)
    postCreationDate= models.DateTimeField(null=True)
    def __str__(self):
        return self.propertyValue

