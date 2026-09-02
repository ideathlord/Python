from feast import Entity, FeatureView, Field
from feast.types import Float32, Int64
from datetime import timedelta
from feast.data_source import FileSource

user = Entity(name="user_id", join_keys=["user_id"])
item = Entity(name="item_id", join_keys=["item_id"])

user_source = FileSource(
    path="../data/features/user_features.csv",
    timestamp_field=None
)

item_source = FileSource(
    path="../data/features/item_features.csv",
    timestamp_field=None
)

user_features_view = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=365),
    schema=[
        Field(name="interaction_count", dtype=Int64),
    ],
    source=user_source
)

item_features_view = FeatureView(
    name="item_features",
    entities=[item],
    ttl=timedelta(days=365),
    schema=[
        Field(name="item_interactions", dtype=Int64),
        Field(name="popularity_score", dtype=Float32),
    ],
    source=item_source
)