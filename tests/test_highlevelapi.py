# OBSS SAHI Tool
# Code written by Fatih C Akyon, 2022.


class TestHighLevelApi:
    def test_bounding_box(self):
        from sahi import BoundingBox

        bbox_minmax = [30.0, 30.0, 100.0, 150.0]
        shift_amount = [50, 40]

        bbox = BoundingBox(bbox_minmax, shift_amount=[0, 0])
        expanded_bbox = bbox.get_expanded_box(ratio=0.1)

        bbox = BoundingBox(bbox_minmax, shift_amount=shift_amount)
        shifted_bbox = bbox.get_shifted_box()

        # compare
        assert expanded_bbox.to_xywh() == [18, 23, 94, 134]
        assert expanded_bbox.to_xyxy() == [18, 23, 112, 157]
        assert shifted_bbox.to_xyxy() == [80, 70, 150, 190]

    def test_category(self):
        from sahi import Category

        category_id = 1
        category_name = "car"
        category = Category(id=category_id, name=category_name)
        assert category.id == category_id
        assert category.name == category_name

    def test_mask(self):
        from sahi import Mask

        coco_segmentation = [[1.0, 1.0, 325.0, 125.0, 250.0, 200.0, 5.0, 200.0]]
        full_shape_height, full_shape_width = 500, 600
        full_shape = [full_shape_height, full_shape_width]

        mask = Mask(segmentation=coco_segmentation, full_shape=full_shape)

        assert mask.full_shape_height == full_shape_height
        assert mask.full_shape_width == full_shape_width
        assert mask.bool_mask[11, 2]

    def test_object_prediction(self):
        from sahi import ObjectPrediction

        bbox = [100, 200, 150, 230]
        coco_bbox = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        category_id = 2
        category_name = "car"
        shift_amount = [0, 0]
        image_height = 1080
        image_width = 1920
        full_shape = [image_height, image_width]

        object_annotation1 = ObjectPrediction(
            bbox=bbox,
            category_id=category_id,
            category_name=category_name,
            shift_amount=shift_amount,
            full_shape=full_shape,
        )

        object_annotation2 = ObjectPrediction.from_coco_annotation_dict(
            annotation_dict={"bbox": coco_bbox, "category_id": category_id, "segmentation": []},
            category_name=category_name,
            full_shape=full_shape,
            shift_amount=shift_amount,
        )

        object_annotation3 = ObjectPrediction.from_coco_bbox(
            bbox=coco_bbox,
            category_id=category_id,
            category_name=category_name,
            full_shape=full_shape,
            shift_amount=shift_amount,
        )

        assert object_annotation1.bbox.minx == bbox[0]
        assert object_annotation1.bbox.miny == bbox[1]
        assert object_annotation1.bbox.maxx == bbox[2]
        assert object_annotation1.bbox.maxy == bbox[3]
        assert object_annotation1.category.id == category_id
        assert object_annotation1.category.name == category_name

        assert object_annotation2.bbox.minx == bbox[0]
        assert object_annotation2.bbox.miny == bbox[1]
        assert object_annotation2.bbox.maxx == bbox[2]
        assert object_annotation2.bbox.maxy == bbox[3]
        assert object_annotation2.category.id == category_id
        assert object_annotation2.category.name == category_name

        assert object_annotation3.bbox.minx == bbox[0]
        assert object_annotation3.bbox.miny == bbox[1]
        assert object_annotation3.bbox.maxx == bbox[2]
        assert object_annotation3.bbox.maxy == bbox[3]
        assert object_annotation3.category.id == category_id
        assert object_annotation3.category.name == category_name

    def test_detection_model(self):
        from sahi import DetectionModel

        MODEL_PATH = "model_path"
        IMAGE_SIZE = 640
        detection_model = DetectionModel(model_path="model_path", image_size=IMAGE_SIZE, load_at_init=False)
        assert detection_model.model_path == MODEL_PATH
        assert detection_model.image_size == IMAGE_SIZE
