from flat_domclick_export_service import FlatCianExportService


if __name__ == "__main__":
    flat_export = FlatCianExportService()
    flat_export.export_flat_info_from_domclick()
    print("finish")

