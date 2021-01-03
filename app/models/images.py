from app import db
from cloudinary.uploader import upload as _cloudinary_upload, destroy as _cloudinary_destroy
from werkzeug.utils import secure_filename as _secure_filename
import os

BASE_CLOUDINARY_URL = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME')}/image/upload"

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String) # reponse['asset_id']
    filename = db.Column(db.String, nullable=False) # response['secure_url'].split('/')[-1:]  #...for profile pics
    version = db.Column(db.String, nullable=False) # response['secure_url'].split('/')[-3:] ##...for profile pics
    public_id = db.Column(db.String, nullable=False) # response['public_id']
    format = db.Column(db.String) # response['format'] ## the filetype e.g. jpg
    caption = db.Column(db.String)
    alt_tag = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=False)
    uploaded_datetime = db.Column(db.DateTime, nullable=True)
    cv_tags = db.Column(db.String)
    

    # posts = db.relationship('Post', secondary=postTags, lazy='dynamic', backref=db.backref('posttags', lazy='dynamic'))

    def __repr__(self):
        return '{} - {}.{}'.format(self.id, self.public_id, self.format)

    def get_all_images(self):
        return Image.query.all()

    def get_postedit_format_photo(self):
        """
        format each image for the posts/post/edit page
        returns e.g. 
        https://res.cloudinary.com/CLOUDINARY_CLOUD_NAME/image/upload/ || v1593793073/ || hlcfxuy4fcveyrlmu6z4 || .gif
        """
        return f"{BASE_CLOUDINARY_URL}/v{self.version}/{self.public_id}.{self.format}"

    def get_all_images_choices():
        imagesList = [(image.asset_id, image.id) for image in Image.query.all()]
        return imagesList

    """
    (Replace version)
    Preview size
    CloudinaryImage("sample.jpg").image(quality=45, width=600, crop="scale")
    https://res.cloudinary.com/dxhxxbycl/image/upload/c_scale,q_45,w_600/sample.jpg
    
    Profile image
    CloudinaryImage("sample.jpg").image(effect="grayscale", height=600, quality=33, width=400, crop="fill")
    https://res.cloudinary.com/dxhxxbycl/image/upload/c_fill,e_grayscale,h_600,q_33,w_400/sample.jpg
    """

    def delete_image(self, **options):
        """
        result = cloudinary.uploader.destroy(public_id, **options)
        _cloudinary_destroy(public_id, **options)
        """
        #first try to delete from cloudinary
        result = _cloudinary_destroy(self.public_id)
        if result and result['result'] == 'ok':
            #delete from db
            db.session.delete(self)
            db.session.commit()
        else:
            print("can't delete: ", result)
        return #something...

    def imageTogglePublic(self):
        if self.is_public:
            self.is_public = False
            return self
        else:
            self.is_public = True
            return self
        

## HELPER - note this is outside of class
def upload_image(files, *args, **kwargs):
    """
    # get uploading status 'content_length', 'content_type', 'filename', 
    # 'headers', 'mimetype', 'mimetype_params', 'name', 'save', 'stream
    folder="profile_pics"
    resource_type="image"
    public_id=filename
    post_id ??
        /// filename = _secure_filename
    """
    for file in files:
        if file.content_type in ['image/gif', 'image/jpeg', 'image/png', 'video/mp4']:
            folder = kwargs.get('folder') or 'blog_post_images'
            upload_result = _cloudinary_upload(file, folder=folder, **kwargs)
            try:
                asset_id = upload_result.get('asset_id')
                filename = upload_result.get('secure_url').split('/')[-1:][0]
                version = upload_result.get('version')
                # secure_url = upload_result.get('secure_url')
                public_id = upload_result.get('public_id')
                format = upload_result.get('format')
                new_image = Image(asset_id=asset_id, filename=filename, version=version, public_id=public_id, format=format)
                db.session.add(new_image)
                db.session.commit()
                if args:
                    args[0].images.append(new_image)
                    db.session.commit()
            except:
                pass ##do something?? db.session.rollback() and maybe delete cloudinary image
        else: 
           # .... we need to tell them no
            pass

## FILTER 
def get_self_image_for_select_buttons(asset_id):
    image = Image.query.filter_by(asset_id=asset_id).first()
    return f"{BASE_CLOUDINARY_URL}/v{image.version}/{image.public_id}.{image.format}"
